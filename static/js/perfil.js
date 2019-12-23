let ctx = document.querySelector('#pick_radar').getContext('2d');
let chart = new Chart(ctx, {
   type: 'radar',
   data: {
   		labels: ['Uno', 'Dos', 'Tres', 'Cuatro', 'Cinco'],
      datasets: [{
         label: '',
         data: [
						10,
						5,
						8,
						2,
						7
					],
					label: '',
					backgroundColor: 'rgba(255, 193, 7, 0.5)',
					borderColor: 'rgba(0, 0, 0, 0)',
					pointBackgroundColor: 'rgba(0, 204, 72, 1)',
          pointBorderColor:'rgba(0, 0, 0, 0)',
          pointRadius: 1
      }]
   },
   options: {
     startAngle: 0,
     legend: {display: false,},
     title: {display: true},
     scale: {
       ticks: {
         display: false,
         min: 0,
         max: 10
       },
       pointLabels:{fontColor:"#fff"},
       angleLines: {color: 'rgba(255,255,255,0.2)'},
       gridLines: {color: 'rgba(255,255,255,0.2)'},
       beginAtZero: true,
       scaleSteps: 10,
       reverse: false
     },
     tooltips: {enabled: false},
     hover: {mode: null},
     
     elements: {
            line: {tension: 0}
     } 
   }
});