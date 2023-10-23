# Static Folder Name
folder_name = "advepa"

dz_array = {
    "public": {
        "favicon": f"{folder_name}/images/advepa/favicon.png",
        "description": "Advepa Educational",
        "og_title": "Advepa Educational",
        "og_description": "Advepa Educational",
        "og_image": f"{folder_name}/images/advepa/favicon.png",
        "title": "Advepa Educational",
    },
    "global": {
        "css": [
            f"{folder_name}/vendor/bootstrap-select/dist/css/bootstrap-select.min.css",
            f"{folder_name}/css/style.css"
        ],

        "js": {
            "top": [
                f"{folder_name}/vendor/global/global.min.js",
                f"{folder_name}/vendor/bootstrap-select/dist/js/bootstrap-select.min.js",
            ],
            "bottom": [
                f"{folder_name}/js/custom.min.js",
                f"{folder_name}/js/dlabnav-init.js",
            ]
        },

    },
    "pagelevel": {
        "advepa": {  # AppName
            "advepa_views": {
                "css": {
                    "index": [
                        f"{folder_name}/vendor/jqvmap/css/jqvmap.min.css",
                        f"{folder_name}/vendor/chartist/css/chartist.min.css",
                        f"{folder_name}/vendor/owl-carousel/owl.carousel.css",
                    ],
                    "index_2": [
                        f"{folder_name}/vendor/jqvmap/css/jqvmap.min.css",
                        f"{folder_name}/vendor/chartist/css/chartist.min.css",
                        f"{folder_name}/vendor/owl-carousel/owl.carousel.css",
                    ],

                    "projects": [
                        f"{folder_name}/vendor/datatables/css/jquery.dataTables.min.css",
                    ],
                    "contacts": [],
                    "kanban": [],
                    "calendar": [
                        f"{folder_name}/vendor/datatables/css/jquery.dataTables.min.css",
                        f"{folder_name}/vendor/fullcalendar-5.11.0/lib/main.css",
                    ],
                    "messages": [],

                    "permissions": [
                        f"{folder_name}/vendor/sweetalert2/dist/sweetalert2.min.css",
                    ],

                    "users": [
                        f"{folder_name}/vendor/sweetalert2/dist/sweetalert2.min.css",
                    ],
                    "add_user": [
                        f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                        f"{folder_name}/vendor/bootstrap-material-datetimepicker/css/bootstrap-material-datetimepicker.css",
                        f"{folder_name}/vendor/jquery-nice-select/css/nice-select.css",
                        f"{folder_name}/vendor/jquery-nice-select/css/nice-select.css",
                        f"{folder_name}/vendor/select2/css/select2.min.css",
                    ],
                    "edit_user": [
                        f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                        f"{folder_name}/vendor/bootstrap-material-datetimepicker/css/bootstrap-material-datetimepicker.css",
                        f"{folder_name}/vendor/jquery-nice-select/css/nice-select.css",
                        f"{folder_name}/vendor/jquery-nice-select/css/nice-select.css",
                        f"{folder_name}/vendor/select2/css/select2.min.css",
                    ],
                    "groups_list": [
                        f"{folder_name}/vendor/sweetalert2/dist/sweetalert2.min.css",
                    ],
                    "assign_permissions_to_user": [

                        f"{folder_name}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/prettify.min.css",
                        f"{folder_name}/vendor/bootstrap-duallistbox/src/bootstrap-duallistbox.css",
                        f"{folder_name}/vendor/bootstrap-duallistbox/dist/bootstrap-duallistbox.css",
                    ],

                    "group_add": [
                        f"{folder_name}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/prettify.min.css",
                        f"{folder_name}/vendor/bootstrap-duallistbox/src/bootstrap-duallistbox.css",
                        f"{folder_name}/vendor/bootstrap-duallistbox/dist/bootstrap-duallistbox.css",
                    ],

                    "group_edit": [
                        f"{folder_name}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/prettify.min.css",
                        f"{folder_name}/vendor/bootstrap-duallistbox/src/bootstrap-duallistbox.css",
                        f"{folder_name}/vendor/bootstrap-duallistbox/dist/bootstrap-duallistbox.css",
                    ],

                    "app_profile": [
                        f"{folder_name}/vendor/lightgallery/css/lightgallery.min.css",
                        f"{folder_name}/vendor/magnific-popup/magnific-popup.css",
                    ],
                    "post_details": [
                        f"{folder_name}/vendor/lightgallery/css/lightgallery.min.css",
                        f"{folder_name}/vendor/magnific-popup/magnific-popup.css"
                    ],

                    "email_compose": [
                        f"{folder_name}/vendor/dropzone/dist/dropzone.css",
                    ],
                    "email_inbox": [],
                    "email_read": [],
                    "app_calender": [
                        f"{folder_name}/vendor/fullcalendar-5.11.0/lib/main.css",
                    ],

                    "ecom_product_grid": [],
                    "ecom_product_list": [
                        f"{folder_name}/vendor/star-rating/star-rating-svg.css",
                    ],
                    "ecom_product_detail": [
                        f"{folder_name}/vendor/star-rating/star-rating-svg.css",
                    ],
                    "ecom_product_order": [],
                    "ecom_checkout": [],
                    "ecom_invoice": [
                        f"{folder_name}/vendor/bootstrap-select/dist/css/bootstrap-select.min.css",
                    ],
                    "ecom_customers": [],

                    "chart_float": [],
                    "chart_morris": [],
                    "chart_chartjs": [],
                    "chart_chartist": [
                        f"{folder_name}/vendor/chartist/css/chartist.min.css"
                    ],
                    "chart_sparkline": [],
                    "chart_peity": [],
                    "uc_select2": [
                        f"{folder_name}/vendor/select2/css/select2.min.css",
                    ],
                    "uc_nestable": [
                        f"{folder_name}/vendor/nestable2/css/jquery.nestable.min.css"
                    ],
                    "uc_noui_slider": [
                        f"{folder_name}/vendor/nouislider/nouislider.min.css"
                    ],
                    "uc_sweetalert": [
                        f"{folder_name}/vendor/sweetalert2/dist/sweetalert2.min.css"
                    ],
                    "uc_toastr": [
                        f"{folder_name}/vendor/toastr/css/toastr.min.css"
                    ],
                    "map_jqvmap": [
                        f"{folder_name}/vendor/jqvmap/css/jqvmap.min.css"
                    ],
                    "uc_lightgallery": [
                        f"{folder_name}/vendor/lightgallery/css/lightgallery.min.css"
                    ],
                    "widget_basic": [
                        f"{folder_name}/vendor/chartist/css/chartist.min.css",
                        f"{folder_name}/vendor/bootstrap-select/dist/css/bootstrap-select.min.css",
                    ],
                    "form_element": [],
                    "form_wizard": [
                        f"{folder_name}/vendor/jquery-smartwizard/dist/css/smart_wizard.min.css"

                    ],
                    "form_editor_ckeditor": [
                        f"{folder_name}/vendor/summernote/summernote.css",
                    ],
                    "form_pickers": [
                        f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                        f"{folder_name}/vendor/clockpicker/css/bootstrap-clockpicker.min.css",
                        f"{folder_name}/vendor/jquery-asColorPicker/css/asColorPicker.min.css",
                        f"{folder_name}/vendor/bootstrap-material-datetimepicker/css/bootstrap-material-datetimepicker.css",
                        f"{folder_name}/vendor/pickadate/themes/default.css",
                        f"{folder_name}/vendor/pickadate/themes/default.date.css",
                    ],
                    "form_validation": [],
                    "table_bootstrap_basic": [],
                    "table_datatable_basic": [
                        f"{folder_name}/vendor/datatables/css/jquery.dataTables.min.css",
                    ],
                    "actions_charts": [
                        f"{folder_name}/vendor/datatables/css/jquery.dataTables.min.css",
                        f"{folder_name}/vendor/select2/css/select2.min.css",
                        f"{folder_name}/vendor/nouislider/nouislider.min.css",
                        f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                        f"{folder_name}/vendor/clockpicker/css/bootstrap-clockpicker.min.css",
                        f"{folder_name}/vendor/jquery-asColorPicker/css/asColorPicker.min.css",
                        f"{folder_name}/vendor/bootstrap-material-datetimepicker/css/bootstrap-material-datetimepicker.css",
                        f"{folder_name}/vendor/pickadate/themes/default.css",
                        f"{folder_name}/vendor/pickadate/themes/default.date.css",
                    ],
                    "access_charts": [
                        f"{folder_name}/vendor/datatables/css/jquery.dataTables.min.css",
                        f"{folder_name}/vendor/select2/css/select2.min.css",
                        f"{folder_name}/vendor/nouislider/nouislider.min.css",
                        f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                        f"{folder_name}/vendor/clockpicker/css/bootstrap-clockpicker.min.css",
                        f"{folder_name}/vendor/jquery-asColorPicker/css/asColorPicker.min.css",
                        f"{folder_name}/vendor/bootstrap-material-datetimepicker/css/bootstrap-material-datetimepicker.css",
                        f"{folder_name}/vendor/pickadate/themes/default.css",
                        f"{folder_name}/vendor/pickadate/themes/default.date.css",
                    ],
                    "page_login": [],
                    "page_register": [],
                    "page_forgot_password": [],
                    "page_lock_screen": [],
                    "page_error_400": [],
                    "page_error_403": [],
                    "page_error_404": [],
                    "page_error_500": [],
                    "page_error_503": [],
                    "empty_page": [],
                },
                "js": {
                    "index": [
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/vendor/owl-carousel/owl.carousel.js",
                        f"{folder_name}/vendor/peity/jquery.peity.min.js",
                        f"{folder_name}/vendor/apexchart/apexchart.js",
                        f"{folder_name}/js/dashboard/dashboard-1.js",

                    ],
                    "index_2": [
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/vendor/owl-carousel/owl.carousel.js",
                        f"{folder_name}/vendor/peity/jquery.peity.min.js",
                        f"{folder_name}/vendor/apexchart/apexchart.js",
                        f"{folder_name}/js/dashboard/dashboard-1.js",
                    ],

                    "projects": [
                        f"{folder_name}/vendor/datatables/js/jquery.dataTables.min.js",
                    ],
                    "contacts": [],
                    "kanban": [
                        f"{folder_name}/vendor/draggable/draggable.js",
                    ],
                    "calendar": [
                        f"{folder_name}/vendor/jqueryui/js/jquery-ui.min.js",
                        f"{folder_name}/vendor/moment/moment.min.js",
                        f"{folder_name}/vendor/fullcalendar-5.11.0/lib/main.min.js",
                        f"{folder_name}/js/plugins-init/fullcalendar-init.js"
                    ],
                    "messages": [],

                    "permissions": [
                        f"{folder_name}/vendor/sweetalert2/dist/sweetalert2.min.js",
                    ],

                    "users": [
                        f"{folder_name}/vendor/sweetalert2/dist/sweetalert2.min.js",

                    ],
                    "add_user": [
                        f"{folder_name}/vendor/jquery-nice-select/js/jquery.nice-select.min.js",
                        f"{folder_name}/vendor/moment/moment.min.js",
                        f"{folder_name}/vendor/bootstrap-material-datetimepicker/js/bootstrap-material-datetimepicker.js",
                        f"{folder_name}/js/plugins-init/material-date-picker-init.js",

                        f"{folder_name}/vendor/select2/js/select2.full.min.js",
                        f"{folder_name}/js/plugins-init/select2-init.js"
                    ],
                    "edit_user": [
                        f"{folder_name}/vendor/jquery-nice-select/js/jquery.nice-select.min.js",
                        f"{folder_name}/vendor/moment/moment.min.js",
                        f"{folder_name}/vendor/bootstrap-material-datetimepicker/js/bootstrap-material-datetimepicker.js",
                        f"{folder_name}/js/plugins-init/material-date-picker-init.js",

                        f"{folder_name}/vendor/select2/js/select2.full.min.js",
                        f"{folder_name}/js/plugins-init/select2-init.js"
                    ],
                    "groups_list": [
                        f"{folder_name}/vendor/sweetalert2/dist/sweetalert2.min.js",
                    ],
                    "assign_permissions_to_user": [
                        f"{folder_name}/vendor/bootstrap-duallistbox/ajax/libs/popper.js/1.12.9/umd/popper.min.js",
                        f"{folder_name}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/run_prettify.js",
                        f"{folder_name}/vendor/bootstrap-duallistbox/dist/jquery.bootstrap-duallistbox.js",
                    ],
                    "group_add": [
                        f"{folder_name}/vendor/bootstrap-duallistbox/ajax/libs/popper.js/1.12.9/umd/popper.min.js",
                        f"{folder_name}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/run_prettify.js",
                        f"{folder_name}/vendor/bootstrap-duallistbox/dist/jquery.bootstrap-duallistbox.js",
                    ],

                    "group_edit": [
                        f"{folder_name}/vendor/bootstrap-duallistbox/ajax/libs/popper.js/1.12.9/umd/popper.min.js",
                        f"{folder_name}/vendor/bootstrap-duallistbox/ajax/libs/prettify/r298/run_prettify.js",
                        f"{folder_name}/vendor/bootstrap-duallistbox/dist/jquery.bootstrap-duallistbox.js",
                    ],

                    "app_profile": [
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/vendor/lightgallery/js/lightgallery-all.min.js",
                        f"{folder_name}/vendor/magnific-popup/jquery.magnific-popup.js",
                    ],
                    "post_details": [
                        f"{folder_name}/vendor/lightgallery/js/lightgallery-all.min.js",
                        f"{folder_name}/vendor/magnific-popup/jquery.magnific-popup.js",
                    ],

                    "email_compose": [
                        f"{folder_name}/vendor/dropzone/dist/dropzone.js",
                    ],
                    "email_inbox": [],
                    "email_read": [],
                    "app_calender": [
                        f"{folder_name}/vendor/jqueryui/js/jquery-ui.min.js",
                        f"{folder_name}/vendor/moment/moment.min.js",
                        f"{folder_name}/vendor/fullcalendar-5.11.0/lib/main.js",
                        f"{folder_name}/js/plugins-init/fullcalendar-init.js"

                    ],
                    "ecom_product_grid": [],
                    "ecom_product_list": [
                        f"{folder_name}/vendor/star-rating/jquery.star-rating-svg.js",
                    ],
                    "ecom_product_detail": [
                        f"{folder_name}/vendor/star-rating/jquery.star-rating-svg.js",
                    ],
                    "ecom_product_order": [],
                    "ecom_checkout": [],
                    "ecom_invoice": [],
                    "ecom_customers": [],

                    "chart_flot": [
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/vendor/apexchart/apexchart.js",
                        f"{folder_name}/vendor/flot/jquery.flot.js",
                        f"{folder_name}/vendor/flot/jquery.flot.pie.js",
                        f"{folder_name}/vendor/flot/jquery.flot.resize.js",
                        f"{folder_name}/vendor/flot-spline/jquery.flot.spline.min.js",
                        f"{folder_name}/js/plugins-init/flot-init.js",
                    ],
                    "chart_morris": [
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/vendor/apexchart/apexchart.js",
                        f"{folder_name}/vendor/raphael/raphael.min.js",
                        f"{folder_name}/vendor/morris/morris.min.js",
                        f"{folder_name}/js/plugins-init/morris-init.js",
                    ],
                    "chart_chartjs": [
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/js/plugins-init/chartjs-init.js",
                    ],
                    "actions_charts": [
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/js/plugins-init/chartjs-init.js",
                        f"{folder_name}/vendor/apexchart/apexchart.js",
                        f"{folder_name}/vendor/datatables/js/jquery.dataTables.min.js",
                        f"{folder_name}/js/plugins-init/datatables.init.js",
                        f"{folder_name}/vendor/select2/js/select2.full.min.js",
                        f"{folder_name}/js/plugins-init/select2-init.js",
                        f"{folder_name}/vendor/nouislider/nouislider.min.js",
                        f"{folder_name}/vendor/wnumb/wNumb.js",
                        f"{folder_name}/js/plugins-init/nouislider-init.js",
                        f"{folder_name}/vendor/bootstrap-select/dist/js/bootstrap-select.min.js",
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/vendor/apexchart/apexchart.js",
                        f"{folder_name}/vendor/moment/moment.min.js",
                        f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.js",
                        f"{folder_name}/vendor/clockpicker/js/bootstrap-clockpicker.min.js",
                        f"{folder_name}/vendor/jquery-asColor/jquery-asColor.min.js",
                        f"{folder_name}/vendor/jquery-asGradient/jquery-asGradient.min.js",
                        f"{folder_name}/vendor/jquery-asColorPicker/js/jquery-asColorPicker.min.js",
                        f"{folder_name}/vendor/bootstrap-material-datetimepicker/js/bootstrap-material-datetimepicker.js",
                        f"{folder_name}/vendor/pickadate/picker.js",
                        f"{folder_name}/vendor/pickadate/picker.time.js",
                        f"{folder_name}/vendor/pickadate/picker.date.js",
                        f"{folder_name}/js/plugins-init/bs-daterange-picker-init.js",
                        f"{folder_name}/js/plugins-init/clock-picker-init.js",
                        f"{folder_name}/js/plugins-init/jquery-asColorPicker.init.js",
                        f"{folder_name}/js/plugins-init/material-date-picker-init.js",
                        f"{folder_name}/js/plugins-init/pickadate-init.js",
                    ],
                    "access_charts": [
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/js/plugins-init/chartjs-init.js",
                        f"{folder_name}/vendor/apexchart/apexchart.js",
                        f"{folder_name}/vendor/datatables/js/jquery.dataTables.min.js",
                        f"{folder_name}/js/plugins-init/datatables.init.js",
                        f"{folder_name}/vendor/select2/js/select2.full.min.js",
                        f"{folder_name}/js/plugins-init/select2-init.js",
                        f"{folder_name}/vendor/nouislider/nouislider.min.js",
                        f"{folder_name}/vendor/wnumb/wNumb.js",
                        f"{folder_name}/js/plugins-init/nouislider-init.js",
                        f"{folder_name}/vendor/bootstrap-select/dist/js/bootstrap-select.min.js",
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/vendor/apexchart/apexchart.js",
                        f"{folder_name}/vendor/moment/moment.min.js",
                        f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.js",
                        f"{folder_name}/vendor/clockpicker/js/bootstrap-clockpicker.min.js",
                        f"{folder_name}/vendor/jquery-asColor/jquery-asColor.min.js",
                        f"{folder_name}/vendor/jquery-asGradient/jquery-asGradient.min.js",
                        f"{folder_name}/vendor/jquery-asColorPicker/js/jquery-asColorPicker.min.js",
                        f"{folder_name}/vendor/bootstrap-material-datetimepicker/js/bootstrap-material-datetimepicker.js",
                        f"{folder_name}/vendor/pickadate/picker.js",
                        f"{folder_name}/vendor/pickadate/picker.time.js",
                        f"{folder_name}/vendor/pickadate/picker.date.js",
                        f"{folder_name}/js/plugins-init/bs-daterange-picker-init.js",
                        f"{folder_name}/js/plugins-init/clock-picker-init.js",
                        f"{folder_name}/js/plugins-init/jquery-asColorPicker.init.js",
                        f"{folder_name}/js/plugins-init/material-date-picker-init.js",
                        f"{folder_name}/js/plugins-init/pickadate-init.js",
                    ],
                    "chart_chartist": [
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/vendor/apexchart/apexchart.js",
                        f"{folder_name}/vendor/chartist/js/chartist.min.js",
                        f"{folder_name}/vendor/chartist-plugin-tooltips/js/chartist-plugin-tooltip.min.js",
                        f"{folder_name}/js/plugins-init/chartist-init.js",
                    ],
                    "chart_sparkline": [
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/vendor/apexchart/apexchart.js",
                        f"{folder_name}/vendor/jquery-sparkline/jquery.sparkline.min.js",
                        f"{folder_name}/js/plugins-init/sparkline-init.js",
                        f"{folder_name}/vendor/svganimation/vivus.min.js",
                        f"{folder_name}/vendor/svganimation/svg.animation.js"
                    ],
                    "chart_peity": [
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/vendor/peity/jquery.peity.min.js",
                        f"{folder_name}/js/plugins-init/piety-init.js",
                    ],

                    "uc_select2": [
                        f"{folder_name}/vendor/select2/js/select2.full.min.js",
                        f"{folder_name}/js/plugins-init/select2-init.js"
                    ],
                    "uc_nestable": [
                        f"{folder_name}/vendor/nestable2/js/jquery.nestable.min.js",
                        f"{folder_name}/js/plugins-init/nestable-init.js"

                    ],
                    "uc_noui_slider": [
                        f"{folder_name}/vendor/nouislider/nouislider.min.js",
                        f"{folder_name}/vendor/wnumb/wNumb.js",
                        f"{folder_name}/js/plugins-init/nouislider-init.js"
                    ],
                    "uc_sweetalert": [
                        f"{folder_name}/vendor/sweetalert2/dist/sweetalert2.min.js",
                        f"{folder_name}/js/plugins-init/sweetalert.init.js",

                    ],
                    "uc_toastr": [
                        f"{folder_name}/vendor/toastr/js/toastr.min.js",
                        f"{folder_name}/js/plugins-init/toastr-init.js"
                    ],
                    "map_jqvmap": [
                        f"{folder_name}/vendor/jqvmap/js/jquery.vmap.min.js",
                        f"{folder_name}/vendor/jqvmap/js/jquery.vmap.world.js",
                        f"{folder_name}/vendor/jqvmap/js/jquery.vmap.usa.js",
                        f"{folder_name}/js/plugins-init/jqvmap-init.js"

                    ],
                    "uc_lightgallery": [
                        f"{folder_name}/vendor/lightgallery/js/lightgallery-all.min.js"

                    ],
                    "widget_basic": [
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/vendor/apexchart/apexchart.js",
                        f"{folder_name}/vendor/chartist/js/chartist.min.js",
                        f"{folder_name}/vendor/chartist-plugin-tooltips/js/chartist-plugin-tooltip.min.js",
                        f"{folder_name}/vendor/flot/jquery.flot.js",
                        f"{folder_name}/vendor/flot/jquery.flot.pie.js",
                        f"{folder_name}/vendor/flot/jquery.flot.resize.js",
                        f"{folder_name}/vendor/flot-spline/jquery.flot.spline.min.js",
                        f"{folder_name}/vendor/jquery-sparkline/jquery.sparkline.min.js",
                        f"{folder_name}/js/plugins-init/sparkline-init.js",
                        f"{folder_name}/vendor/peity/jquery.peity.min.js",
                        f"{folder_name}/js/plugins-init/piety-init.js",
                        f"{folder_name}/js/plugins-init/widgets-script-init.js",
                    ],
                    "form_element": [],
                    "form_wizard": [
                        f"{folder_name}/vendor/jquery-validation/jquery.validate.min.js",
                        f"{folder_name}/js/plugins-init/jquery.validate-init.js",
                        f"{folder_name}/vendor/jquery-smartwizard/dist/js/jquery.smartWizard.js",
                    ],
                    "form_editor_ckeditor": [
                        f"{folder_name}/vendor/ckeditor/ckeditor.js",
                        f"{folder_name}/js/plugins-init/summernote-init.js",

                    ],
                    "form_pickers": [
                        f"{folder_name}/vendor/bootstrap-select/dist/js/bootstrap-select.min.js",
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/vendor/apexchart/apexchart.js",
                        f"{folder_name}/vendor/moment/moment.min.js",
                        f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.js",
                        f"{folder_name}/vendor/clockpicker/js/bootstrap-clockpicker.min.js",
                        f"{folder_name}/vendor/jquery-asColor/jquery-asColor.min.js",
                        f"{folder_name}/vendor/jquery-asGradient/jquery-asGradient.min.js",
                        f"{folder_name}/vendor/jquery-asColorPicker/js/jquery-asColorPicker.min.js",
                        f"{folder_name}/vendor/bootstrap-material-datetimepicker/js/bootstrap-material-datetimepicker.js",
                        f"{folder_name}/vendor/pickadate/picker.js",
                        f"{folder_name}/vendor/pickadate/picker.time.js",
                        f"{folder_name}/vendor/pickadate/picker.date.js",
                        f"{folder_name}/js/plugins-init/bs-daterange-picker-init.js",
                        f"{folder_name}/js/plugins-init/clock-picker-init.js",
                        f"{folder_name}/js/plugins-init/jquery-asColorPicker.init.js",
                        f"{folder_name}/js/plugins-init/material-date-picker-init.js",
                        f"{folder_name}/js/plugins-init/pickadate-init.js",
                    ],
                    "form_validation": [
                        f"{folder_name}/vendor/jquery-validation/jquery.validate.min.js",
                        f"{folder_name}/js/plugins-init/jquery.validate-init.js",
                    ],
                    "table_bootstrap_basic": [],
                    "table_datatable_basic": [
                        f"{folder_name}/vendor/chart.js/Chart.bundle.min.js",
                        f"{folder_name}/vendor/apexchart/apexchart.js",
                        f"{folder_name}/vendor/datatables/js/jquery.dataTables.min.js",
                        f"{folder_name}/js/plugins-init/datatables.init.js",
                    ],
                    "page_login": [],
                    "page_register": [],
                    "page_forgot_password": [],
                    "page_lock_screen": [],
                    "page_error_400": [],
                    "page_error_403": [],
                    "page_error_404": [],
                    "page_error_500": [],
                    "page_error_503": [],
                    "empty_page": [],

                },
            }
        }
    }

}
