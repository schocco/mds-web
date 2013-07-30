'''
module for gpx conversion tasks
'''
from apps.trails.models import Trail
from django.contrib.gis.gdal.geometries import OGRGeometry
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.utils.layermapping import LayerMapError
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import os
import sys



class GPXMapping(LayerMapping):
    '''
    3d Layer Mapping.
    
    Assuming a Django model with a LineString field called 'waypoints' and a
    GPX file test.gpx this class can be used as follows:
    
    track_mapping = {'waypoints' : 'LINESTRING'}
    gpx_file = 'test.gpx'

    lm = GPXMapping(Trail, gpx_file, track_mapping, layer=1)
    lm.save(verbose=True)
    '''
    # Snippet taken from http://djangosnippets.org/snippets/1800/
    def __init__(self, *args, **kwargs):
        # Setting this environment variable tells OGR to use the elevation
        # attribute as the Z coordinate value on the geometries.  See:
        #  http://www.gdal.org/ogr/drv_gpx.html
        os.environ['GPX_ELE_AS_25D'] = 'YES'
        super(GPXMapping, self).__init__(*args, **kwargs)
        # Unset the environment variable, so it doesn't affect other
        # GPX DataSource objects.
        os.environ.pop('GPX_ELE_AS_25D')
        
    def get_values(self, verbose=False, fid_range=False, step=False,
         progress=False, silent=False, stream=sys.stdout, strict=False):
        """
        Returns the contents from the OGR DataSource Layer 
        according to the mapping dictionary given at initialization.

        Keyword Parameters:
         verbose:
           If set, information will be printed subsequent to each model save
           executed on the database.

         fid_range:
           May be set with a slice or tuple of (begin, end) feature ID's to map
           from the data source.  In other words, this keyword enables the user
           to selectively import a subset range of features in the geographic
           data source.

         step:
           If set with an integer, transactions will occur at every step
           interval. For example, if step=1000, a commit would occur after
           the 1,000th feature, the 2,000th feature etc.

         progress:
           When this keyword is set, status information will be printed giving
           the number of features processed and sucessfully saved.  By default,
           progress information will pe printed every 1000 features processed,
           however, this default may be overridden by setting this keyword with an
           integer for the desired interval.

         stream:
           Status information will be written to this file handle.  Defaults to
           using `sys.stdout`, but any object with a `write` method is supported.

         silent:
           By default, non-fatal error notifications are printed to stdout, but
           this keyword may be set to disable these notifications.

         strict:
           Execution of the model mapping will cease upon the first error
           encountered.  The default behavior is to attempt to continue.
        """     
        # Getting the default Feature ID range.
        default_range = self.check_fid_range(fid_range)

        # Setting the progress interval, if requested.
        if progress:
            if progress is True or not isinstance(progress, int):
                progress_interval = 1000
            else:
                progress_interval = progress

        # Defining the 'real' get values method, utilizing the transaction
        # decorator created during initialization.
        @self.transaction_decorator
        def _get_values(feat_range=default_range, num_feat=0, num_saved=0):
            if feat_range:
                layer_iter = self.layer[feat_range]
            else:
                layer_iter = self.layer

            for feat in layer_iter:
                num_feat += 1
                # Getting the keyword arguments
                try:
                    kwargs = self.feature_kwargs(feat)
                except LayerMapError, msg:
                    # Something borked the validation
                    if strict: raise
                    elif not silent:
                        stream.write('Ignoring Feature ID %s because: %s\n' % (feat.fid, msg))
                else:
                    # Constructing the model using the keyword args
                    is_update = False
                    if self.unique:
                        # If we want unique models on a particular field, handle the
                        # geometry appropriately.
                        try:
                            # Getting the keyword arguments and retrieving
                            # the unique model.
                            u_kwargs = self.unique_kwargs(kwargs)
                            m = self.model.objects.using(self.using).get(**u_kwargs)
                            is_update = True

                            # Getting the geometry (in OGR form), creating
                            # one from the kwargs WKT, adding in additional
                            # geometries, and update the attribute with the
                            # just-updated geometry WKT.
                            geom = getattr(m, self.geom_field).ogr
                            new = OGRGeometry(kwargs[self.geom_field])
                            for g in new: geom.add(g)
                            setattr(m, self.geom_field, geom.wkt)
                        except ObjectDoesNotExist:
                            # No unique model exists yet, create.
                            m = self.model(**kwargs)
                    else:
                        m = self.model(**kwargs)

                    try:
                        # Attempting to save.
                        pippo = kwargs

                        num_saved += 1
                        if verbose: stream.write('%s: %s\n' % (is_update and 'Updated' or 'Saved', m))
                    except SystemExit:
                        raise
                    except Exception, msg:
                        if self.transaction_mode == 'autocommit':
                            # Rolling back the transaction so that other model saves
                            # will work.
                            transaction.rollback_unless_managed()
                        if strict:
                            # Bailing out if the `strict` keyword is set.
                            if not silent:
                                stream.write('Failed to save the feature (id: %s) into the model with the keyword arguments:\n' % feat.fid)
                                stream.write('%s\n' % kwargs)
                            raise
                        elif not silent:
                            stream.write('Failed to save %s:\n %s\nContinuing\n' % (kwargs, msg))

                # Printing progress information, if requested.
                if progress and num_feat % progress_interval == 0:
                    stream.write('Processed %d features, saved %d ...\n' % (num_feat, num_saved))

            # Only used for status output purposes -- incremental saving uses the
            # values returned here.
            return pippo

        nfeat = self.layer.num_feat
        if step and isinstance(step, int) and step < nfeat:
            # Incremental saving is requested at the given interval (step)
            if default_range:
                raise LayerMapError('The `step` keyword may not be used in conjunction with the `fid_range` keyword.')
            beg, num_feat, num_saved = (0, 0, 0)
            indices = range(step, nfeat, step)
            n_i = len(indices)

            for i, end in enumerate(indices):
                # Constructing the slice to use for this step; the last slice is
                # special (e.g, [100:] instead of [90:100]).
                if i + 1 == n_i: step_slice = slice(beg, None)
                else: step_slice = slice(beg, end)

                try:
                    pippo = _get_values(step_slice, num_feat, num_saved)
                    beg = end
                except:
                    stream.write('%s\nFailed to save slice: %s\n' % ('=-' * 20, step_slice))
                    raise
        else:
            # Otherwise, just calling the previously defined _save() function.
            return _get_values()

def gpx_to_linestring(gpx_file):
    '''
    utility method to convert a gpx file to a LineString object
    '''
    track_mapping = {'waypoints' : 'LINESTRING'}
    lm = GPXMapping(Trail, gpx_file, track_mapping, layer=1)
    return  lm.get_values()['waypoints']

   
        
