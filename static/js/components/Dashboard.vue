<template>
    <div class="">
        <div class="d-flex align-items-center justify-content-between">
            <h2>Dashboard</h2>
        </div>
        <div class="alert alert-success alert-dismissible fade show" role="alert" v-if="successMessage">
            {{ successMessage }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div class="alert alert-danger alert-dismissible fade show" role="alert" v-if="errorMessage">
            {{ errorMessage }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div class="row justify-content-center">
            <div class="col-12 order-2 order-md-3 order-lg-2 mb-4">
                <div class="card">
                    <h5 class="card-header m-0 me-2 pb-3">{{ this.moodYear }} Mood</h5>
                    <div class="row">
                        <div class="col-6 ms-3">
                            <vue-datepicker v-model="moodYear" auto-apply year-picker
                                @update:model-value="moodYearSelected()" />
                        </div>

                    </div>
                    <apexchart type="bar" height="350" :options="moodChartOptions" :series="moodSeries"></apexchart>
                </div>
            </div>
            <!-- <div class="col-12 col-md-8 col-lg-4 order-3 order-md-2">
                <div class="row"></div>
            </div> -->
        </div>
        <div class="row justify-content-center">
            <div class="col-lg-6 col-xl-6 order-0 mb-4">
                <div class="card h-100">
                    <h5 class="card-header m-0 me-2 pb-3">Your Cycle</h5>
                    <div class="card-body">

                        <apexchart width="380" type="donut" :options="cycleChartOptions" :series="cycleSeries"
                            v-if="cycleSeries.length > 0"></apexchart>
                        <div class="" v-else>
                            <div class="text-dark">
                                <p><strong>No period data available.</strong></p>
                                <p>It looks like you haven't logged any period data yet. To get insights into your menstrual cycle, start logging your periods using our app.</p>
                                <p><em>Feel free to explore other features in the meantime!</em></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-6 col-xl-6 order-0 mb-4">
                <div class="card h-100">
                    <div class="card-header d-flex align-items-center justify-content-between pb-0 mb-3">
                        <div class="card-title mb-0">
                            <h5 class="m-0 me-2">Your Period Statistics</h5>
                            <!-- <small class="text-muted" v-if="cycleYear">{{ cycleYear }}</small>
                            <small class="text-muted" v-else>Overall</small> -->
                        </div>
                        <!-- <div class="dropdown">
                            <button class="btn p-0" type="button" id="orederStatistics" data-bs-toggle="dropdown"
                                aria-haspopup="true" aria-expanded="false">
                                <i class="bx bx-dots-vertical-rounded"></i>
                            </button>
                            <div class="dropdown-menu dropdown-menu-end" aria-labelledby="orederStatistics">
                                <a class="dropdown-item" href="javascript:void(0);">Select All</a>
                                <a class="dropdown-item" href="javascript:void(0);">Refresh</a>
                                <a class="dropdown-item" href="javascript:void(0);">Share</a>
                            </div>
                        </div> -->
                    </div>
                    <div class="card-body">
                        <!-- <div class="d-flex justify-content-between align-items-center mb-3">
                            <div class="d-flex flex-column align-items-center gap-1">
                                <h2 class="mb-2">8,258</h2>
                                <span>Total Orders</span>
                            </div>
                            <div id="orderStatisticsChart"></div>
                        </div> -->
                        <ul class="p-0 m-0" v-if="averageCycleLength !== 0 && averagePeriodLength !== 0 && averagePeriodDuration !== 0">
                            <li class="d-flex mb-4 pb-1">
                                <div class="avatar flex-shrink-0 me-3">
                                    <span class="avatar-initial rounded bg-label-primary">
                                        <i class="fa-solid fa-rotate"></i>
                                    </span>
                                </div>
                                <div class="d-flex w-100 flex-wrap align-items-center justify-content-between gap-2">
                                    <div class="me-2">
                                        <h6 class="mb-0">Average Cycle Length</h6>
                                        <small class="text-muted">Typical length of full menstrual cycle</small>
                                    </div>
                                    <div class="user-progress">
                                        <small class="fw-semibold">{{ averageCycleLength }} days</small>
                                    </div>
                                </div>
                            </li>
                            <li class="d-flex mb-4 pb-1">
                                <div class="avatar flex-shrink-0 me-3">
                                    <span class="avatar-initial rounded bg-label-danger">
                                        <i class="fa-solid fa-droplet"></i>
                                    </span>
                                </div>
                                <div class="d-flex w-100 flex-wrap align-items-center justify-content-between gap-2">
                                    <div class="me-2">
                                        <h6 class="mb-0">Average Intermenstrual Period</h6>
                                        <small class="text-muted">Typical duration between periods</small>
                                    </div>
                                    <div class="user-progress">
                                        <small class="fw-semibold">{{ averagePeriodLength }} days</small>
                                    </div>
                                </div>
                            </li>
                            <li class="d-flex mb-4 pb-1">
                                <div class="avatar flex-shrink-0 me-3">
                                    <span class="avatar-initial rounded bg-label-info">
                                        <i class="fa-solid fa-droplet-slash"></i>
                                    </span>
                                </div>
                                <div class="d-flex w-100 flex-wrap align-items-center justify-content-between gap-2">
                                    <div class="me-2">
                                        <h6 class="mb-0">Average Period Duration</h6>
                                        <small class="text-muted">Typical duration of menstrual bleeding</small>
                                    </div>
                                    <div class="user-progress">
                                        <small class="fw-semibold">{{ averagePeriodDuration }} days</small>
                                    </div>
                                </div>
                            </li>

                        </ul>
                        <div class="" v-else>
                            <div class="text-dark">
                                <p><strong>No period data available.</strong></p>
                                <p>We currently don't have enough data to calculate accurate statistics. Consider logging more period-related information for meaningful insights.</p>
                                <p><em>Feel free to explore other features in the meantime!</em></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row justify-content-center">
            <div class="col-lg-6 col-xl-6 order-0 mb-4">
                <div class="card h-100">
                    <div class="card-header d-flex align-items-center justify-content-between pb-0 mb-3">
                        <div class="card-title mb-0">
                            <h5 class="m-0 me-2">Upcoming Appointments <span v-if="upcomingAppointments.length">({{
                                upcomingAppointments.length }})</span></h5>
                            <!-- <small class="text-muted" v-if="cycleYear">{{ cycleYear }}</small>
                            <small class="text-muted" v-else>Overall</small> -->
                        </div>

                    </div>
                    <div class="card-body">
                        <ul class="timeline" v-if="upcomingAppointments.length">
                            <li v-for="app in upcomingAppointments" class="timeline-item timeline-item-transparent">
                                <span class="timeline-point-wrapper"><span
                                        class="timeline-point timeline-point-info"></span></span>
                                <div class="timeline-event">
                                    <div class="timeline-header">
                                        <h6 class="mb-0">{{ app.title }}</h6>
                                        <span class="text-muted">{{ app.date }}</span>
                                        <span class="text-muted" v-if="app.time">{{ formatTime(app.time, 'LT') }}</span>
                                        <span class="text-muted" v-else>All Day</span>
                                    </div>
                                    <p>{{ app.location }}</p>
                                    <hr />
                                    <div class="d-flex justify-content-between flex-wrap gap-2">
                                        <div class="d-flex flex-wrap">
                                            <div class="avatar me-3">
                                                <i class="fa-solid fa-user-nurse"></i>
                                                <i class="fa-solid fa-stethoscope"></i>
                                            </div>
                                            <div>
                                                <p class="mb-0">{{ app.doctor }}</p>
                                                <!-- <span class="text-muted">Javascript Developer</span> -->
                                            </div>
                                        </div>
                                        <div class="d-flex flex-wrap align-items-center cursor-pointer">
                                            <!-- <i class="bx bx-message me-2"></i>
                                            <i class="bx bx-phone-call"></i> -->
                                        </div>
                                    </div>
                                </div>
                            </li>
                            <li class="timeline-end-indicator">
                                <i class="bx bx-check-circle"></i>
                            </li>
                        </ul>
                        <div class="" v-else>
                            <div class="text-dark">
                                <p><strong>No upcoming appointments.</strong></p>
                                <p>It looks like you haven't logged any period data yet. To get insights into your menstrual cycle, start logging your periods using our app.</p>
                                <p><em>Feel free to explore other features in the meantime!</em></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-6 col-xl-6 order-0 mb-4">
                <div class="card h-100">
                    <div class="card-header d-flex align-items-center justify-content-between pb-0 mb-3">
                        <div class="card-title mb-0">
                            <h5 class="m-0 me-2">Your Appointment Statistics</h5>
                        </div>
                    </div>
                    <div class="card-body">
                        <ul class="p-0 m-0">
                            <li class="d-flex mb-4 pb-1">
                                <div class="avatar flex-shrink-0 me-3">
                                    <span class="avatar-initial rounded bg-label-primary">
                                        <i class='bx bx-run'></i>
                                    </span>
                                </div>
                                <div class="d-flex w-100 flex-wrap align-items-center justify-content-between gap-2">
                                    <div class="me-2">
                                        <h6 class="mb-0">Total</h6>
                                        <small class="text-muted"></small>
                                    </div>
                                    <div class="user-progress">
                                        <small class="fw-semibold">{{ totalMedicalAppointments + totalPersonalAppointments +
                                            totalWorkAppointments }}</small>
                                    </div>
                                </div>
                            </li>
                            <li class="d-flex mb-4 pb-1">
                                <div class="avatar flex-shrink-0 me-3">
                                    <span class="avatar-initial rounded bg-label-secondary">
                                        <i class='bx bx-briefcase'></i>
                                    </span>
                                </div>
                                <div class="d-flex w-100 flex-wrap align-items-center justify-content-between gap-2">
                                    <div class="me-2">
                                        <h6 class="mb-0">Work</h6>
                                        <small class="text-muted"></small>
                                    </div>
                                    <div class="user-progress">
                                        <small class="fw-semibold">{{ totalWorkAppointments }}</small>
                                    </div>
                                </div>
                            </li>
                            <li class="d-flex mb-4 pb-1">
                                <div class="avatar flex-shrink-0 me-3">
                                    <span class="avatar-initial rounded bg-label-info">
                                        <i class='bx bx-cool'></i>
                                    </span>
                                </div>
                                <div class="d-flex w-100 flex-wrap align-items-center justify-content-between gap-2">
                                    <div class="me-2">
                                        <h6 class="mb-0">Personal</h6>
                                        <small class="text-muted"></small>
                                    </div>
                                    <div class="user-progress">
                                        <small class="fw-semibold">{{ totalPersonalAppointments }}</small>
                                    </div>
                                </div>
                            </li>
                            <li class="d-flex mb-4 pb-1">
                                <div class="avatar flex-shrink-0 me-3">
                                    <span class="avatar-initial rounded bg-label-warning">
                                        <i class='bx bx-capsule'></i>
                                    </span>
                                </div>
                                <div class="d-flex w-100 flex-wrap align-items-center justify-content-between gap-2">
                                    <div class="me-2">
                                        <h6 class="mb-0">Medical</h6>
                                        <small class="text-muted"></small>
                                    </div>
                                    <div class="user-progress">
                                        <small class="fw-semibold">{{ totalMedicalAppointments }}</small>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template> 
<script>
import { ref } from 'vue'
import moment from 'moment'
export default {
    name: 'Calendar',
    props: [],
    data: function () {
        return {
            successMessage: '',
            errorMessage: '',
            moodSeries: [{
                name: 'Happy',
                data: []
            }, {
                name: 'Sad',
                data: []
            }, {
                name: 'Neutral',
                data: []
            }],
            moodChartOptions: {
                chart: {
                    type: 'bar',
                    height: 350,
                    stacked: true,
                    // stackType: '100%'
                },
                plotOptions: {
                    bar: {
                        columnWidth: '20%',
                    }
                },
                colors: ['#ff3e1d', '#03c3ec', '#adb5bd'],
                responsive: [{
                    breakpoint: 480,
                    options: {
                        legend: {
                            position: 'bottom',
                            offsetX: -10,
                            offsetY: 0
                        }
                    }
                }],
                xaxis: {
                    categories: [],
                },
                fill: {
                    opacity: 1
                },
                legend: {
                    position: 'right',
                    offsetX: 0,
                    offsetY: 50
                },
            },
            cycleChartOptions: {
                colors: ['#ff3e1d', '#03c3ec'],
                labels: ['Menstruation', 'Intermenstrual Interval'],
                dataLabels: {
                    enabled: true,
                    formatter(value, opts) {
                        console.log(value);
                        console.log(opts);
                        return opts.w.config.series[opts.seriesIndex] + ' days';
                    },
                },
                plotOptions: {
                    pie: {
                        donut: {
                            labels: {
                                show: true,
                                name: {
                                    show: true,
                                    fontSize: '22px',
                                },
                                value: {
                                    show: true,
                                    fontSize: '16px',
                                    formatter(value, opts) {
                                        return value + ' days';
                                    },
                                },
                                total: {
                                    show: true,
                                    label: 'Full Cycle',
                                    formatter(value, opts) {
                                        return value.config.series.reduce((a, b) => a + b, 0) + ' days';
                                    },
                                }
                            }
                        }
                    }
                }
            },
            cycleSeries: [],
            moodYear: new Date().getFullYear(),
            cycleYear: new Date().getFullYear(),
            averagePeriodDuration: 'N/A',
            averageCycleLength: 'N/A',
            averagePeriodLength: 'N/A',
            upcomingAppointments: [],
            totalMedicalAppointments: 0,
            totalWorkAppointments: 0,
            totalPersonalAppointments: 0,
        };
    },
    computed: {

    },
    watch: {

        moodSeries: {
            handler: function (newValue, oldValue) {
                //console.log(newValue);

            },
            deep: true,
            immediate: true
        },
    },
    methods: {
        formatTime(time, format) {
            return moment(time, 'HH:mm:ss').format(format);
        },
        openDateDetailsModal() {
            $('#dateDetailsModal').modal('show');
        },
        hideDateDetailsModal() {
            $('#dateDetailsForm')[0].reset();
            $('#dateDetailsModal').modal('hide');
        },
        getMoodDataForChart() {
            let url = '../get_mood_data_for_chart/' + this.moodYear;
            this.axios.get(url).then(response => {
                console.log(response.data.series);
                this.moodChartOptions = {
                    ...this.moodChartOptions,
                    xaxis: {
                        categories: response.data.categories
                    }
                };
                this.moodSeries = response.data.series;
                response.data.data.forEach(element => {

                });

            }).catch(error => {
                console.log(error);
            });
        },
        moodYearSelected() {
            //console.log(this.moodYear);
            this.getMoodDataForChart();
        },
        getPeriodDataForChart() {
            let url = '../get_period_data_for_chart/';
            this.axios.get(url).then(response => {
                const hasUserInput = response.data && (
                    response.data.average_cycle_length !== 0 ||
                    response.data.average_period_length !== 0 ||
                    response.data.average_period_duration !== 0
                );

                if (hasUserInput) {
                    console.log(response.data);
                    this.averageCycleLength = response.data.average_cycle_length;
                    this.averagePeriodLength = response.data.average_period_length;
                    this.averagePeriodDuration = response.data.average_period_duration;
                    this.cycleSeries = [this.averagePeriodDuration, this.averagePeriodLength];
                } else {
                    // Handle the case where the user has not logged any period data
                    // Set default values or display a message
                    this.averageCycleLength = 'N/A';
                    this.averagePeriodLength = 'N/A';
                    this.averagePeriodDuration = 'N/A';
                    this.cycleSeries = [];
                }

                // console.log(response.data);
                // this.averageCycleLength = response.data.average_cycle_length;
                // this.averagePeriodLength = response.data.average_period_length;
                // this.averagePeriodDuration = response.data.average_period_duration;
                // this.cycleSeries = [this.averagePeriodDuration, this.averagePeriodLength];
            }).catch(error => {
                console.log(error);
            });
        },
        getAppointmentDataForChart() {
            let url = '../get_appointment_data_for_chart/';
            this.axios.get(url).then(response => {
                console.log(response.data);
                this.upcomingAppointments = response.data.appointments;
                this.totalMedicalAppointments = response.data.stats.total_medical;
                this.totalPersonalAppointments = response.data.stats.total_personal;
                this.totalWorkAppointments = response.data.stats.total_work;
            }).catch(error => {
                console.log(error);
                //console.log(error.response.data);
            });
        },

    },
    created() {
        this.getMoodDataForChart();
        this.getPeriodDataForChart();
        this.getAppointmentDataForChart();
    },
    mounted() {

    }

} 
</script>