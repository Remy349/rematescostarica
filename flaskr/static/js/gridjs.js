document.addEventListener('DOMContentLoaded', () => {
  const adminPagosTablaPaypal = document.getElementById('adminPagosTablaPaypal')

  const updateUrl = (prev, query) => {
    return (
      prev +
      (prev.indexOf('?') >= 0 ? '&' : '?') +
      new URLSearchParams(query).toString()
    )
  }

  if (adminPagosTablaPaypal) {
    new gridjs.Grid({
      columns: [
        { id: 'firstname', name: 'Nombre' },
        { id: 'firstLastname', name: '1er Apellido', width: '200px' },
        { id: 'secondLastname', name: '2do Apellido', width: '200px' },
        { id: 'email', name: 'Correo' },
        { id: 'courseName', name: 'Curso' },
        { id: 'grossAmount', name: 'Cantidad Bruta $', width: '230px' },
        { id: 'paypalFee', name: 'Comisión de PayPal $', width: '270px' },
        { id: 'netAmount', name: 'Cantidad Neta $', width: '230px' },
        { id: 'date', name: 'Fecha de Compra', width: '250px' },
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
            moment(`${d.date}`).format('L'),
          ]),
        total: (result) => result.total,
      },
      search: {
        enable: true,
        server: {
          url: (prev, search) => {
            return updateUrl(prev, { search })
          },
        },
      },
      pagination: {
        enable: true,
        limit: 10,
      },
      language: {
        search: {
          placeholder: 'Escribe para buscar...',
        },
        sort: {
          sortAsc: 'Orden de columna ascendente.',
          sortDesc: 'Orden de columna descendente.',
        },
        pagination: {
          previous: 'Anterior',
          next: 'Siguiente',
          navigate: (page, pages) => `Página ${page} de ${pages}`,
          page: (page) => `Página ${page}`,
          showing: 'Mostrando del',
          of: 'de',
          to: 'al',
          results: 'registros',
        },
        loading: 'Cargando...',
        noRecordsFound: 'Sin coincidencias encontradas.',
        error: 'Ocurrió un error al obtener los datos.',
      },
    }).render(adminPagosTablaPaypal)
  }
})
