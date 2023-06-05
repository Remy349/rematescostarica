document.addEventListener('DOMContentLoaded', () => {
  const adminPagosTablaPaypal = document.getElementById('adminPagosTablaPaypal')

  if (adminPagosTablaPaypal) {
    new gridjs.Grid({
      columns: [
        { id: 'firstname', name: 'Nombre' },
        { id: 'firstLastname', name: '1er Apellido' },
        { id: 'secondLastname', name: '2do Apellido' },
        { id: 'email', name: 'Correo' },
        { id: 'courseName', name: 'Curso' },
        { id: 'grossAmount', name: 'Cantidad Bruta $' },
        { id: 'paypalFee', name: 'Comisión de PayPal $' },
        { id: 'netAmount', name: 'Cantidad Neta $' },
        { id: 'date', name: 'Fecha de Compra' },
      ],
      server: {
        url: '/admin/pagos/paypal/data',
        then: (result) =>
          result.data.map((d) => [
            d.firstname,
            d.firstLastname,
            d.secondLastname,
            d.email,
            d.courseName,
            d.grossAmount,
            d.paypalFee,
            d.netAmount,
            d.date,
          ]),
        total: (result) => result.total,
      },
      pagination: {
        enable: true,
        limit: 10,
      },
    }).render(adminPagosTablaPaypal)
  }
})
