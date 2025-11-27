from django.db import models

class Pedido(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('LISTO', 'Listo'),
        ('ENTREGADO', 'Entregado'),
    ]

    nombre_cliente = models.CharField("Nombre del cliente", max_length=100)
    telefono = models.CharField("Teléfono", max_length=20, blank=True)
    tipo_tamal = models.CharField("Tipo de tamal", max_length=100)
    cantidad = models.PositiveIntegerField("Cantidad de tamales")
    comentarios = models.TextField("Comentarios / indicaciones", blank=True)
    estado = models.CharField(
        "Estado",
        max_length=10,
        choices=ESTADOS,
        default='PENDIENTE'
    )
    fecha_creacion = models.DateTimeField("Fecha de pedido", auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre_cliente} - {self.tipo_tamal} x{self.cantidad}"
