# ===================================================
# Clases encargadas del API relacionado a Feria
#
# Author: Tyron Fonseca - tyron.fonseca@ucr.ac.cr
# Last modified: 24/11/2021
# ===================================================

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from ferias.models import Feria
from api.serializers.feria_serializer import FeriaSerializer
from api.views.utils import DynamicFieldsViewMixin, FeriasHelper


class FeriaList(DynamicFieldsViewMixin, generics.ListAPIView):
    ''' Retornar una lista con todas las ferias '''
    queryset = Feria.objects.all()
    serializer_class = FeriaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['provincia', 'canton', 'distrito',
                        'horarios__dia_inicio', 'horarios__dia_final',
                        'horarios__hora_inicio', 'horarios__hora_final']
    search_fields = ['nombre', 'provincia',
                     'canton', 'distrito', 'horarios__dia_inicio',
                     'horarios__dia_final']

    def get_queryset(self):
        ferias_id_filtered = []
        ferias = Feria.objects.all()
        # Parametros del URL
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        radius = self.request.query_params.get('radius')
        # Filtrar por latitud, longitud y radio
        if lat is not None and lon is not None and radius is not None:
            index = 0
            for feria in ferias.iterator():
                # Verificar si esta en el radio
                if FeriasHelper.is_in_radius(float(lat), float(lon),
                                             feria.latitud, feria.longitud,
                                             int(radius)):
                    # Agregar ID de la feria
                    ferias_id_filtered.insert(index, feria.ferias_id)
                    index = index + 1
            # Filtrar las ferias que esten es el radio dado
            return ferias.filter(ferias_id__in=ferias_id_filtered)
        else:
            # Devolver todas las ferias si falta alguno de los parametros
            return ferias


class FeriaDetail(DynamicFieldsViewMixin, generics.RetrieveAPIView):
    '''Traer de la base de datos una feria dado su ID (pk)'''
    queryset = Feria.objects.all()
    serializer_class = FeriaSerializer
