"use strict";
var KTDatatablesBasicBasic = function() {

	// Base Table for all Datatables
	/* BASE TABLE BEGINS */
	/* BASE TABLE ENDS */
	

	/* BASE TABLE BEGINS */
	var initTable = function() {
		var table = $('#nt_datatable');

		table.DataTable({
			// Order settings
			order: [[0, 'asc']],

			columnDefs: [
				{ orderable: false, targets: [-1] }
			 ],
		});

		
		$('#searchbar').on( 'keyup', function () {
			table.DataTable().search(this.value).draw();
		} );
		
	};
	/* BASE TABLE ENDS */

	
	/* BASE TABLE BEGINS */
	var initTableSmall = function() {
		var table = $('#nt_datatable_small');

		table.DataTable({
			ordering: false,
		});
	};
	/* BASE TABLE ENDS */

	return {

		//main function to initiate the module
		init: function() {
			initTable();
			initTableSmall();
		}
	};
}();

jQuery(document).ready(function() {
	KTDatatablesBasicBasic.init();
});
