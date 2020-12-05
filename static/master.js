function filterTable() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  for (i=0; i<tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      }
      else {
        tr[i].style.display = "none";
      }
    }
  }
}

$(document).ready(function() {
  $("td:nth-child(5)").each(function() {
    if ($(this).text() === "SS") {
      $(this).parent().addClass("red");
    }
    else {
      $(this).parent().addClass("white");
    }
  });
});

$(document).ready(function() {
  $("td:nth-child(3)").each(function() {
    if ($(this).text() === "IC") {
      $(this).parent().addClass("red");
    }
    else if ($(this).text() === "CC") {
      $(this).parent().addClass("green");
    }
  });
});

$(document).ready(function() {
  $("td:nth-child(2)").each(function() {
    if ($(this).text() === "--") {
      $(this).parent().addClass("red");
    }
    else if ($(this).text() === "-") {
      $(this).parent().addClass("green");
    }
  });
});

$(document).ready(function() {
    $('#apara-table').DataTable( {
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'pdfHtml5',
                download: 'open'
            }
        ]
    } );
} );