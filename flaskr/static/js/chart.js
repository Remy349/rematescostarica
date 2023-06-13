document.addEventListener('DOMContentLoaded', () => {
  // ========================>
  const adminDashboardIndexCharts = async () => {
    const res = await fetch('/admin/dashboard/data', {
      method: 'GET',
    })

    const data = await res.json()

    const adminIndexPieChart = document.getElementById('adminIndexPieChart')
    const adminIndexLineChart = document.getElementById('adminIndexLineChart')

    new Chart(adminIndexLineChart, {
      type: 'line',
      data: {
        labels: data.line.labels,
        datasets: [
          {
            label: 'Ingresos',
            data: data.line.data,
            fill: true,
            tension: 0.1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      },
    })

    new Chart(adminIndexPieChart, {
      type: 'doughnut',
      data: {
        labels: data.pie.labels,
        datasets: [
          {
            label: 'Usuarios',
            data: data.pie.data,
            backgroundColor: [
              'rgb(255, 99, 132)',
              'rgb(54, 162, 235)',
              'rgb(255, 205, 86)',
            ],
            hoverOffset: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      },
    })
  }

  const adminIndexCharts = document.getElementById('adminIndexCharts')

  if (adminIndexCharts && window.location.pathname === '/admin/dashboard') {
    adminDashboardIndexCharts()
  }
})
