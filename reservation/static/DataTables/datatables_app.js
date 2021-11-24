
let lang_url = {
    "language": {
        "url": "/reservation/rest/datatables_lang"
    }
};

function tableKwargs(order, sort) {
    return {
        "language": {
            "url": "/reservation/rest/datatables_lang"
        },
        "order": [[order, sort]]
    }
}

$(document).ready(function() {
    $('#detailTable').DataTable(tableKwargs(0,"asc"));
    $('#listTable').DataTable(lang_url);
    $('#ownersTable').DataTable(tableKwargs(0,"asc"));
    $('#clientsTable').DataTable(tableKwargs(0,"asc"));
    $('#productsTable').DataTable(tableKwargs(0,"asc"));
    $('#contractsTable').DataTable(tableKwargs(0,"asc"));
    $('#villasTable').DataTable(tableKwargs(0,"asc"));
    $('#trainsTable').DataTable(tableKwargs(0,"asc"));
})
