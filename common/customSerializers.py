from rest_framework_gis.serializers import GeometryField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class GeometryPointFieldSerializerFields(GeometryField):

    def to_internal_value(self, value):
        try:
            value = value.split(",")
        except:
            raise ValidationError(
                _("Enter the co-ordinates in (latitude,longitude). Ex-12,13")
            )
        try:
            latitude = float(value[0])
        except ValueError:
            raise ValidationError(
                _("Enter the co-ordinates in (latitude,longitude). Ex-12,13")
            )
        try:
            longitude = float(value[1])
        except ValueError:
            raise ValidationError(
                _("Enter the co-ordinates in (latitude,longitude). Ex-12,13")
            )
        value = {
            "type": "Point",
            "coordinates": [longitude, latitude]
        }
        value = json.dumps(value)
        try:
            return GEOSGeometry(value)
        except (ValueError, GEOSException, OGRException, TypeError):
            raise ValidationError(
                _('Invalid format: string or unicode input unrecognized as GeoJSON, WKT EWKT or HEXEWKB.'))

    def to_representation(self, value):
        """ """
        value = super(
            GeometryPointFieldSerializerFields, self).to_representation(value)
        # change to compatible with google map
        data = {
            "type": "Point",
            "coordinates": [
                value['coordinates'][1], value['coordinates'][0]
            ]
        }
        return data