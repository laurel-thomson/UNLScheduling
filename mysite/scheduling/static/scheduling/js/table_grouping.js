$(document).ready( function () {
    var groupColumn = 0;
    $('table.group').DataTable({
        "columnDefs": [
            { "visible": false, "targets": groupColumn }
        ],
        "order": [[ groupColumn, 'asc' ]],
        "autoWidth": false,
        "paging": false,
        "ordering": false,
        "info": false,
        "drawCallback": function ( settings ) {
            var api = this.api();
            var rows = api.rows( {page:'current'} ).nodes();
            var last=null;
 
            api.column(groupColumn, {page:'current'} ).data().each( function ( group, i ) {
                if ( last !== group ) {
                    $(rows).eq( i ).before(
                        '<tr class="group"><td colspan="5">'+group+'</td></tr>'
                    );
 
                    last = group;
                }
            } );
        }
    } );
    $('table.nongroup').DataTable({
        "autoWidth": false,
        "paging": false,
        "ordering": false,
        "searching": false,
        "info": false,
    });
} );