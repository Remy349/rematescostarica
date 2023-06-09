document.addEventListener('DOMContentLoaded', () => {
  const adminPagosTablaPaypal = document.getElementById('adminPagosTablaPaypal')
  const adminCursosTabla = document.getElementById('adminCursosTabla')
  const adminUsuariosTabla = document.getElementById('adminUsuariosTabla')

  const updateUrl = (prev, query) => {
    return (
      prev +
      (prev.indexOf('?') >= 0 ? '&' : '?') +
      new URLSearchParams(query).toString()
    )
  }

  if (adminUsuariosTabla) {
    new gridjs.Grid({
      columns: [
        { id: 'firstname', name: 'Nombre' },
        { id: 'firstLastname', name: '1re Apellido', width: '200px' },
        { id: 'secondLastname', name: '2do Apellido', width: '200px' },
        { id: 'email', name: 'Correo' },
        { id: 'phoneNumber', name: 'Teléfono' },
        { id: 'courseName', name: 'Curso' },
        { id: 'joinedIn', name: 'Fecha de Registro', width: '250px' },
        { id: 'isActive', name: 'Estado', width: '150px' },
      ],
      server: {
        url: '/admin/usuarios/data',
        then: (result) =>
          result.data.map((d) => [
            d.firstname,
            d.firstLastname,
            d.secondLastname,
            d.email,
            d.phoneNumber,
            d.courseName,
            moment(`${d.joinedIn}`).format('L'),
            gridjs.html(
              d.isActive
                ? `<a class='admin__usuarios-tabla_status true' href='/admin/usuarios/estado/${d.userId}'>Activo</a>`
                : `<a class='admin__usuarios-tabla_status false' href='/admin/usuarios/estado/${d.userId}'>Inactivo</a>`
            ),
          ]),
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
    }).render(adminUsuariosTabla)
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

  if (adminCursosTabla) {
    new gridjs.Grid({
      columns: [
        { id: 'firstname', name: 'Nombre' },
        { id: 'firstLastname', name: '1re Apellido', width: '200px' },
        { id: 'secondLastname', name: '2do Apellido', width: '200px' },
        { id: 'email', name: 'Correo' },
        { id: 'phoneNumber', name: 'Teléfono' },
        { id: 'joinedIn', name: 'Fecha de Registro', width: '250px' },
        { id: 'isActive', name: 'Estado', width: '150px' },
      ],
      server: {
        url: '/admin/cursos/data',
        then: (result) =>
          result.data.map((d) => [
            d.firstname,
            d.firstLastname,
            d.secondLastname,
            d.email,
            d.phoneNumber,
            moment(`${d.joinedIn}`).format('L'),
            gridjs.html(d.isActive ? 'Activo' : 'Inactivo'),
          ]),
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
    }).render(adminCursosTabla)
  }
})
