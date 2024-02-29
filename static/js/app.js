
// // import Vue from 'vue';
// // window.Vue = Vue;
// Vue.component('example-component', require('./components/ExampleComponent.vue').default);

// const app = new Vue({
//     delimiters: ['[[', ']]'],
//     el: '#app',
//     data: {
//         title: 'Welcome to My Journal'
//     }
// })

globalThis.__VUE_OPTIONS_API__ = true;
globalThis.__VUE_PROD_DEVTOOLS__ = true;


// import "bootstrap/dist/css/bootstrap.min.css"
// import "bootstrap"
import { createApp, ref } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import axios from 'axios';
import flatPickr from 'vue-flatpickr-component';
import VueApexCharts from "vue3-apexcharts";
import VueDatePicker from '@vuepic/vue-datepicker';
// import DataTable from 'datatables.net-vue3';
// import DataTablesCore from 'datatables.net-bs5';
import PrimeVue from 'primevue/config';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Dropdown from 'primevue/dropdown';
import Timeline from 'primevue/timeline';

// DataTable.use(DataTablesCore);

//import BootstrapVue from 'bootstrap-vue';
// Vue.use(BootstrapVue)
const app = createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            title: 'Welcome to My Site'
            
        }
      }
})

app.config.globalProperties.axios = axios;
app.config.globalProperties.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
let token = document.getElementsByName("csrfmiddlewaretoken");

if (token && token[0]) {
    app.config.globalProperties.axios.defaults.headers.common['X-CSRFToken'] = token[0].value;
} else {
    console.error('CSRF token not found: https://docs.djangoproject.com/en/3.0/ref/csrf/#ajax');
}
app.use(PrimeVue);

app.component('dashboard', require('./components/Dashboard.vue').default);
app.component('calendar', require('./components/Calendar.vue').default);
app.component('appointments', require('./components/Appointments.vue').default);
app.component('intercourses', require('./components/Intercourses.vue').default);
app.component('contacts', require('./components/Contacts.vue').default);
app.component('sleep', require('./components/Sleep.vue').default);
app.component('physical-activities', require('./components/PhysicalActivities.vue').default);
app.component('full-calendar', FullCalendar);
app.component('flat-pickr', flatPickr);
app.component('apexchart', VueApexCharts);
app.component('vue-datepicker', VueDatePicker);
app.component('primvevue-data-table', DataTable);
app.component('primvevue-column', Column);
app.component('primvevue-dropdown', Dropdown);
app.component('primvevue-timeline', Timeline);

app.mount('#app');