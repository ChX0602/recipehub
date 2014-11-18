function addStep() {
    // Get table of steps
    var steps = document.getElementById("step-table");
    var numRows = steps.rows.length;
    var row = steps.insertRow(numRows);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    cell1.innerHTML = "<input class='form-control' maxlength='200' name='des" + numRows + "' type='text' />";
    cell2.innerHTML = "<input class='form-control' max='60' min='0' name='preptime" + numRows + "' placeholder='0' type='number' />";
    cell3.innerHTML = "<input class='form-control' max='60' min='0' name='cooktime" + numRows + "' placeholder='0' type='number' />";
    cell4.innerHTML = "<input type='file' name='stepPic" + numRows + "' class='btn btn-success'>";
}

function addIngredient() {
    // Get table of steps
    var steps = document.getElementById("ingredient-table");
    var numRows = steps.rows.length;
    var row = steps.insertRow(numRows);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    cell1.innerHTML = "<input class='form-control' maxlength='20' name='item" + numRows + "' type='text' />";
    cell2.innerHTML = "<input class='form-control' min='0' name='quantity" + numRows + "' type='number' />";
    cell3.innerHTML = "<input class='form-control' maxlength='20' name='unit" + numRows + "' type='text' />";
    cell4.innerHTML = "<input class='form-control' maxlength='200' name='notes" + numRows + "' type='text' />";
}