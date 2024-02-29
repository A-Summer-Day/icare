<template>
    <div class="container">
        <div class="alert alert-success alert-dismissible fade show" role="alert" v-if="successMessage">
            {{ successMessage }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div class="alert alert-danger alert-dismissible fade show" role="alert" v-if="errorMessage">
            {{ errorMessage }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <!-- <div class="d-grid mb-4" style="grid-template-columns: 125px; grid-row-gap: 5px;">
            <div class="badge" style="background-color: #e83e8c; width: "><i class='bx bx-droplet'></i><i class='bx bx-droplet'></i><i class='bx bx-droplet'></i></div>
            <div class="badge " style="background-color: purple;"><i class='bx bx-heart'></i><i class='bx bx-heart'></i><i class='bx bx-heart'></i></div>
            <div class="badge" style="background-color: green; font-size: 1.15rem;">Appointment</div>
        </div> -->
        <div class="d-flex mb-4 align-items-center" style="">
            <div class="d-flex align-items-center me-4">
                <div class="badge me-2" style="background-color: #e83e8c; width: "><i class='bx bx-droplet'></i><i
                        class='bx bx-droplet'></i><i class='bx bx-droplet'></i></div>
                <div style="color: #e83e8c;">Menstrual Days</div>
            </div>
            <div class="d-flex align-items-center">
                <div class="badge me-2" style="background-color: purple; width: "><i class='bx bx-heart'></i><i
                        class='bx bx-heart'></i><i class='bx bx-heart'></i></div>
                <div style="color: purple;">Intimacy Days</div>
            </div>
        </div>
        <div class="row justify-content-center">
            <div class="col-12">
                <full-calendar :options="calendarOptions">
                    <template v-slot:eventContent='arg'>
                        <div v-if="arg.event.extendedProps.source == 'mood'">
                            <div class="capitalize">
                                {{ arg.event.title }}
                                <i v-if="arg.event.extendedProps.mood == 'HAPPY'" class='bx bx-happy-beaming'></i>
                                <i v-if="arg.event.extendedProps.mood == 'SAD'" class='bx bx-sad'></i>
                                <i v-if="arg.event.extendedProps.mood == 'NEUTRAL'" class='bx bx-meh'></i>
                            </div>
                        </div>
                        <div v-else-if="arg.event.extendedProps.source == 'appointment'">
                            <div class="capitalize" data-bs-toggle="modal" data-bs-target="#appointmentDetails">
                                {{ arg.event.title }}
                            </div>
                        </div>
                        <div v-else-if="arg.event.extendedProps.source == 'cycle'">
                            <i class='bx bx-droplet'></i><i class='bx bx-droplet'></i><i class='bx bx-droplet'></i>
                        </div>
                        <div v-else-if="arg.event.extendedProps.source == 'intercourse'">
                            <i class='bx bx-heart'></i><i class='bx bx-heart'></i><i class='bx bx-heart'></i>
                        </div>
                        <!-- <div v-else>
                            &nbsp;
                        </div> -->
                    </template>
                </full-calendar>
                <div class="modal fade" id="appointmentDetails" tabindex="-1" aria-labelledby="appointmentDetailsLabel"
                    aria-hidden="true">
                    <div class="modal-dialog modal-sm" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="appointmentDetailsLabel">{{ appointmentDetails.title }}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                                </button>
                            </div>
                            <div class="modal-body">
                                <p>Doctor: <span v-if="appointmentDetails.doctor">{{ appointmentDetails.doctor
                                }}</span><span v-else>N/A</span></p>
                                <p>Location: <a v-if="appointmentDetails.location"
                                        :href="`https://maps.google.com/?q=${appointmentDetails.location}`" target="_blank">
                                        {{ appointmentDetails.location }}</a><span v-else>N/A</span></p>

                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal fade" id="dateDetailsModal" ref="dateDetailsModal" tabindex="-1"
                    aria-labelledby="dateDetailsLabel" aria-hidden="true">
                    <div class="modal-dialog" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="dateDetailsLabel">{{ dateToView }}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                                </button>
                            </div>
                            <div class="modal-body">
                                <form id="dateDetailsForm">
                                    <div class="row mb-3">
                                        <label for="logPeriod" class="col-sm-3 col-form-label">Log Period</label>
                                        <div class="col-sm-9">
                                            <input class="form-check-input" type="checkbox" id="logPeriod"
                                                v-model="logPeriod">
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <label for="moodToLog" class="col-sm-3 col-form-label">Mood</label>
                                        <div class="col-sm-9">
                                            <select class="form-select" aria-label="Select a mood" v-model="moodToLog">
                                                <option value="" selected>Select a mood</option>
                                                <option value="HAPPY">Happy</option>
                                                <option value="SAD">Sad</option>
                                                <option value="NEUTRAL">Neutral</option>
                                            </select>
                                        </div>
                                    </div>
                                </form>

                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="button" class="btn btn-primary" @click="updateDateDetails">Save</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal fade" id="addAppointmentModal" tabindex="-1" aria-labelledby="" aria-hidden="true">
                    <div class="modal-dialog" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="">Add an appointment</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                                </button>
                            </div>
                            <div class="modal-body">
                                <form id="addAppointmentForm">
                                    <div class="row mb-3">
                                        <label for="flatpickr-date" class="col-sm-3 col-form-label">Date</label>
                                        <div class="col-sm-9">
                                            <input type="text" class="form-control" placeholder="YYYY-MM-DD" name="date"
                                                v-model="appointmentDate" id="flatpickr-date" />

                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <label for="appointmentTitle" class="col-sm-3 col-form-label">Appointment</label>
                                        <div class="col-sm-9">
                                            <input type="text" class="form-control" id="appointmentTitle" name="title"
                                                v-model="appointmentTitle">
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <label for="appointmentDoctor" class="col-sm-3 col-form-label">Doctor</label>
                                        <div class="col-sm-9">
                                            <input type="text" class="form-control" id="appointmentDoctor" name="doctor"
                                                v-model="appointmentDoctor">
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <label for="appointmentLocation" class="col-sm-3 col-form-label">Location</label>
                                        <div class="col-sm-9">
                                            <input type="text" class="form-control" id="appointmentLocation" name="location"
                                                v-model="appointmentLocation">
                                        </div>
                                    </div>
                                </form>

                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="button" class="btn btn-primary" @click="addAppointment">Save</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template> 
<script>
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import { formatDate } from '@fullcalendar/core'
import momentPlugin from '@fullcalendar/moment'
import moment from 'moment'
// import flatpickr from 'flatpickr'
// import 'flatpickr/dist/flatpickr.css';

export default {
    name: 'Calendar',
    props: [],
    data: function () {
        return {
            calendarOptions: {
                plugins: [dayGridPlugin, interactionPlugin, momentPlugin],
                initialView: 'dayGridMonth',
                dayMaxEvents: true, // allow "more" link when too many events
                dateClick: this.handleDateClick,
                eventClick: this.handleEventClick,
                eventMouseEnter: this.handleEventMouseEnter,
                eventMouseLeave: this.handleEventMouseLeave,
                eventsSet: this.handleEvents,
                eventSources: [],
                //events: [],
                // headerToolbar: {
                //     left: 'title',
                //     center: 'openAddAppointmentModal',
                //     right: 'today prev,next'
                // },
                // customButtons: {
                //     openAddAppointmentModal: {
                //         text: 'Add Appointment',
                //         click: () => this.openAddAppointmentModal()
                //     }
                // },
            },
            appointmentDetails: {
                title: '',
                location: '',
                doctor: ''
            },
            dateToView: null,
            logPeriod: false,
            moodToLog: '',
            //addAppointment: true,
            appointmentDate: '',
            appointmentTitle: '',
            appointmentDoctor: '',
            appointmentLocation: '',
            mood: [],
            cycles: [],
            appointments: [],
            intercourses: [],
            successMessage: '',
            errorMessage: ''
        };
    },
    computed: {
        events() {
            return [].concat.apply([], [this.cycles, this.mood, this.appointments]);
        }
    },
    watch: {
        calendarOptions: {
            handler: function (newValue, oldValue) {
                //console.log(newValue);
            },
            deep: true,
            immediate: true
        },
        logPeriod: {
            handler: function (newValue, oldValue) {
                //console.log(newValue);

            },
            deep: true,
            immediate: true
        },
        moodToLog: {
            handler: function (newValue, oldValue) {
                //console.log(newValue);

            },
            deep: true,
            immediate: true
        },
        dateToView: {
            handler: function (newValue, oldValue) {
                //console.log(newValue);


            },
            deep: true,
            immediate: true
        }
    },
    methods: {
        handleDateClick(arg) {
            console.log('date click! ' + arg.date)
            console.log(formatDate(arg.date, {
                month: '2-digit',
                day: '2-digit',
                year: 'numeric',
            }))
            //console.log(moment(arg.date).format('YYYY-MM-DD'))
            this.dateToView = moment(arg.date).format('YYYY-MM-DD')

            //console.log(arg.date);    


            this.openDateDetailsModal();
        },
        handleEventClick(info) {
            if (info.event.extendedProps.source == 'appointment') {
                this.appointmentDetails.title = info.event.title;
                this.appointmentDetails.doctor = info.event.extendedProps.doctor;
                this.appointmentDetails.location = info.event.extendedProps.location;
                $('#appointmentDetails').modal('show');
            } else if (info.event.extendedProps.source == 'intercourse') {
                // do something?
            }
        },
        handleEvents(events) {
            //console.log('handleEvents')
        },
        handleEventMouseEnter(info) {
            // console.log('mouseEnter');
            // console.log(info);
        },
        handleEventMouseLeave(info) {
            // console.log('mouseLeave');
            // console.log(info);
        },
        openDateDetailsModal() {
            let periodLogged = this.cycles.find(c => c.date == this.dateToView);
            //console.log(periodLogged);
            this.logPeriod = periodLogged !== undefined ? true : false;
            //console.log(this.logPeriod);


            let moodLogged = this.mood.find(c => c.date == this.dateToView);
            this.moodToLog = moodLogged != undefined ? moodLogged.mood : '';
            //console.log(moodLogged);
            //console.log(this.moodToLog);
            $('#dateDetailsModal').modal('show');
        },
        hideDateDetailsModal() {
            // console.log('hideAddAppointment');
            // $('#addAppointmentForm')[0].reset();
            console.log('hide date details modal');
            $('#dateDetailsForm')[0].reset();
            $('#dateDetailsModal').modal('hide');
        },
        getMood() {
            let url = '../get_mood/';
            this.axios.get(url).then(response => {
                //console.log(response.data);
                response.data.mood.forEach(element => {
                    element.title = element.mood;
                });

                this.mood = response.data.mood;
                //this.mood = this.mood.map(obj => ({ ...obj, display: 'list-item', className: obj.mood == 'HAPPY' ? 'mood-happy' : obj.mood == 'SAD' ? 'mood-sad' : 'mood-neutral' }))

                let happy = response.data.mood.filter(element => element.mood == 'HAPPY');
                let sad = response.data.mood.filter(element => element.mood == 'SAD');
                let neutral = response.data.mood.filter(element => element.mood == 'NEUTRAL');


                //this.calendarOptions.events.push(...this.mood);
                this.calendarOptions.eventSources.push({
                    events: happy,
                    borderColor: 'red',
                    color: 'red',
                    display: 'list-item',
                    className: 'mood-happy'
                });
                this.calendarOptions.eventSources.push({
                    events: sad,
                    color: 'grey',
                    display: 'list-item',
                    className: 'mood-sad'
                });
                this.calendarOptions.eventSources.push({
                    events: neutral,
                    color: 'blue',
                    display: 'list-item',
                    className: 'mood-neutral'
                });

            }).catch(error => {
                console.log(error);
            });
        },
        getCycles() {
            let url = '../get_cycles/';
            this.axios.get(url).then(response => {
                //console.log('done');
                //console.log(response.data);
                this.cycles = response.data.cycles;
                //this.cycles = this.cycles.map(obj => ({ ...obj, color: '#e83e8c' }));
                //this.calendarOptions.events.push(...this.cycles);
                //console.log(this.calendarOptions.events);
                this.calendarOptions.eventSources.push({
                    events: response.data.cycles,
                    color: '#e83e8c'
                });

            }).catch(error => {
                console.log(error);
            });
        },
        getAppointments() {
            let url = '../get_appointments/';
            this.axios.get(url).then(response => {
                //console.log(response.data);
                this.appointments = response.data.appointments;
                //this.appointments = this.appointments.map(obj => ({ ...obj, color: 'green' }))
                this.calendarOptions.eventSources.push({
                    events: response.data.appointments,
                    color: 'green'
                });
                //this.calendarOptions.events.push(...this.appointments);

            }).catch(error => {
                console.log(error);
            });
        },
        getIntercourses() {
            let url = '../get_intercourses/';
            this.axios.get(url).then(response => {
                //console.log(response.data);
                this.intercourses = response.data.intercourses;
                //this.appointments = this.appointments.map(obj => ({ ...obj, color: 'green' }))
                this.calendarOptions.eventSources.push({
                    events: response.data.intercourses,
                    color: 'purple'
                });

            }).catch(error => {
                console.log(error);
            });
        },
        addAppointment() {
            console.log('appointment added');
            let url = '../save_appointment/';
            let data = new FormData()
            data.append('date', this.appointmentDate)
            data.append('title', this.appointmentTitle)
            data.append('doctor', this.appointmentDoctor)
            data.append('location', this.appointmentLocation)
            this.axios.post(url, data).then(response => {
                console.log(response.data)
                if (response.data.success) {
                    this.successMessage = response.data.message;
                    this.getAppointments();
                    $('#addAppointmentModal').modal('hide');
                    $('#addAppointmentForm')[0].reset();
                }

            }).catch(error => {
                console.log(error);
            });

        },
        updateDateDetails() {
            let url = '../update_date_details/';
            let data = new FormData();
            data.append('logPeriod', this.logPeriod);
            data.append('moodToLog', this.moodToLog);
            data.append('date', this.dateToView);
            this.axios.post(url, data).then(response => {
                console.log(response.data)
                if (response.data.success) {
                    this.successMessage = response.data.message;
                    // this.$nextTick(() => {
                    //     this.fetachCalendarData();
                    // });
                    this.fetachCalendarData();
                    this.hideDateDetailsModal();
                }

            }).catch(error => {
                console.log(error);
            });

        },
        fetachCalendarData() {
            this.calendarOptions.eventSources = [];
            this.getCycles();
            this.getMood();
            this.getAppointments();
            this.getIntercourses();
        }
    },
    created() {
        // this.getCycles();
        // this.getMood();
        // this.getAppointments();
        this.fetachCalendarData();
    },
    mounted() {
        console.log('Component mounted.');
        //flatpickr('#flatpickr-date')
        new flatpickr('#flatpickr-date', {
            minDate: 'today'
        })

        const modal = document.getElementById('dateDetailsModal');

        modal.addEventListener('hide.bs.modal', () => {
            //$('#dateDetailsForm')[0].reset();
            this.logPeriod = false;
            this.moodToLog = '';
        })
    }

} 
</script>