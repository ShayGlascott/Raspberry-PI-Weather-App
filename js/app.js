const SQL = window.SQL;

const db = new SQL.Database();

const xhr = new XMLHttpRequest();
xhr.open('GET', '../weatherData.db', true);
xhr.responseType = 'arraybuffer';

xhr.onload = function () {
  const uInt8Array = new Uint8Array(this.response);
  db.open(uInt8Array);

  const result = db.exec('SELECT * FROM weather ORDER BY timestamp DESC LIMIT 25');

  const labels = result[0].columns;
  const rows = result[0].values;

  const datasets = labels.map((label, index) => ({
    label: label,
    data: rows.map(row => row[index]),
    backgroundColor: 'rgba(75, 192, 192, 0.2)',
    borderColor: 'rgba(75, 192, 192, 1)',
    borderWidth: 1
  }));

  const ctx = document.getElementById('myChart').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: rows.map((_, index) => `Row ${index + 1}`), 
      datasets: datasets
    },
  });
};

xhr.send();