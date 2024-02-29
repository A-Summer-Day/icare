<template>
    <div class="container">
        <div class="d-flex align-items-center justify-content-between">
            <h2>Appointments</h2>
            <button type="button" class="btn btn-primary" @click="openAddAppointmentModal(null)"> Add Appointment</button>
        </div>


        <div class="alert alert-success alert-dismissible fade show mt-2" role="alert" v-if="successMessage">
            {{ successMessage }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div class="alert alert-danger alert-dismissible fade show mt-2" role="alert" v-if="errorMessage">
            {{ errorMessage }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div class="row justify-content-center">
            <div class="col-12">
                <div class="nav-align-top">
                    <ul class="nav nav-tabs" role="tablist">
                        <li class="nav-item">
                            <button type="button" class="nav-link active" role="tab" data-bs-toggle="tab"
                                data-bs-target="#navs-upcoming-appointments" aria-controls="navs-upcoming-appointments"
                                aria-selected="true">
                                Upcoming
                            </button>
                        </li>
                        <li class="nav-item">
                            <button type="button" class="nav-link" role="tab" data-bs-toggle="tab"
                                data-bs-target="#navs-past-appointments" aria-controls="navs-past-appointments"
                                aria-selected="false">
                                Past
                            </button>
                        </li>

                    </ul>
                    <div class="tab-content">
                        <div class="tab-pane fade show active" id="navs-upcoming-appointments" role="tabpanel">
                            <div class="row">
                                <div class="col col-md-4 mt-3" v-for="appointment in upcomingAppointments">
                                    <div class="card h-100 shadow-none bg-transparent border border-primary" style="">

                                        <div class="card-body">
                                            <div class="d-flex justify-content-between mb-3">
                                                <h5 class="card-title">{{ appointment.title }}</h5>
                                                <div>
                                                    <a href="javascript:void(0);" class="card-close mx-1"
                                                        @click="openAddAppointmentModal(appointment)" title="Edit">
                                                        <i class='bx bxs-edit'></i>
                                                    </a>
                                                    <a href="javascript:void(0);" class="card-close mx-1"
                                                        @click="confirmDelete(appointment.id)" title="Delete">
                                                        <!-- <i class="tf-icons bx bx-x"></i> -->
                                                        <i class='bx bx-trash'></i>
                                                    </a>
                                                </div>

                                            </div>
                                            <h6 class="card-subtitle text-muted">
                                                {{ formatDate(appointment.date, 'll') }}
                                            </h6>
                                            <small v-if="appointment.time" class="card-subtitle mb-2 text-muted">
                                                {{ formatTime(appointment.time, 'LT') }}
                                            </small>
                                            <small v-else class="card-subtitle mb-2 text-muted">All Day</small>
                                            <div class="mt-2">
                                                <p class="card-text mb-1">Doctor: <span v-if="appointment.doctor">
                                                        {{ appointment.doctor }}
                                                    </span><span v-else>N/A</span>
                                                </p>
                                                <p class="card-text mb-1">
                                                    Location: <a v-if="appointment.location"
                                                        :href="`https://maps.google.com/?q=${appointment.location}`"
                                                        target="_blank"> {{ appointment.location }}</a>
                                                    <span v-else>N/A</span>
                                                </p>
                                            </div>

                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="tab-pane fade" id="navs-past-appointments" role="tabpanel">
                            <div class="row">
                                <div class="col col-md-4 mt-3" v-for="appointment in pastAppointments">
                                    <div class="card h-100 shadow-none bg-transparent border border-primary" style="">

                                        <div class="card-body">
                                            <div class="d-flex justify-content-between mb-3">
                                                <h5 class="card-title">{{ appointment.title }}</h5>
                                                <!-- <a href="javascript:void(0);" class="card-close" @click="confirmDelete(appointment.id)">
                                                    <i class="tf-icons bx bx-x"></i>
                                                </a> -->
                                            </div>
                                            <h6 class="card-subtitle mb-2 text-muted">{{ formatDate(appointment.date, 'll')
                                            }}
                                            </h6>
                                            <p class="card-text">Doctor: <span v-if="appointment.doctor">{{
                                                appointment.doctor
                                            }}</span><span v-else>N/A</span>
                                            </p>
                                            <p class="card-text">Location: <a v-if="appointment.location"
                                                    :href="`https://maps.google.com/?q=${appointment.location}`"
                                                    target="_blank">
                                                    {{ appointment.location }}</a><span v-else>N/A</span>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="saveAppointmentModal" tabindex="-1" aria-labelledby="saveAppointmentModalLabel"
            aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="">{{ saveAppointmentModalTitle }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                        </button>
                    </div>
                    <div class="modal-body">
                        <form id="saveAppointmentForm">

                            <div class="row mb-3">
                                <label for="flatpickr-date" class="col-sm-3 col-form-label">Date</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" placeholder="YYYY-MM-DD" name="date"
                                        v-model="appointmentDate" id="flatpickr-date" />

                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="flatpickr-time" class="col-sm-3 col-form-label">Time</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" placeholder="HH:MM" name="time"
                                        v-model="appointmentTime" id="flatpickr-time" />

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
        <div class="modal fade" id="confirmDeletetModal" tabindex="-1" aria-labelledby="confirmDeletetModalLabel"
            aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="">Confirm delete</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                        </button>
                    </div>
                    <div class="modal-body">
                        <p>Are you sure you want to delete this appointment?</p>

                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-danger" @click="deleteAppointment">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template> 
<script>

import moment from 'moment'

export default {
    name: 'Appointments',
    props: [],
    data: function () {
        return {
            appointmentId: '',
            appointmentDate: '',
            appointmentTime: '',
            appointmentTitle: '',
            appointmentDoctor: '',
            appointmentLocation: '',
            appointmentIdToDelete: null,
            appointments: [],
            successMessage: '',
            errorMessage: '',
        };
    },
    computed: {
        upcomingAppointments() {
            return this.appointments.filter(a => !moment(a.date).isBefore(moment(), 'day'));
        },
        pastAppointments() {
            return this.appointments.filter(a => moment(a.date).isBefore(moment(), 'day'));
        },
        saveAppointmentModalTitle() {
            return this.appointmentId ? 'Edit Appointment' : 'Add Appointment';
        }
    },
    methods: {
        formatDate(date, format) {
            //console.log(date);
            return moment(date).format(format);
        },
        formatTime(time, format) {
            return moment(time, 'HH:mm:ss').format(format);
        },
        openAddAppointmentModal(appointment = null) {
            console.log(appointment);
            if (appointment != null) {
                this.appointmentId = appointment.id;
                this.appointmentTitle = appointment.title;
                this.appointmentDate = appointment.date;
                this.appointmentTime = appointment.time;
                this.appointmentDoctor = appointment.doctor;
                this.appointmentLocation = appointment.location;
            }
            //this.saveAppointmentModalTitle = this.appointmentId ? 'Edit Appointment' : 'Add Appointment';
            $('#saveAppointmentModal').modal('show');
        },
        hideAddAppointmentModal() {
            $('#saveAppointmentForm')[0].reset();
            $('#saveAppointmentModal').modal('hide');
        },
        getAppointments() {
            let url = '../get_appointments/';
            this.axios.get(url).then(response => {
                this.appointments = response.data.appointments;


            }).catch(error => {
                console.log(error);
            });
        },
        addAppointment() {
            let url = this.appointmentId ? '../update_appointment/' : '../save_appointment/';
            let data = new FormData()
            if (this.appointmentId) {
                data.append('id', this.appointmentId);
            }
            data.append('date', this.appointmentDate)
            data.append('time', this.appointmentTime)
            data.append('title', this.appointmentTitle)
            data.append('doctor', this.appointmentDoctor)
            data.append('location', this.appointmentLocation)
            this.axios.post(url, data).then(response => {
                console.log(response.data)
                if (response.data.success) {
                    this.successMessage = response.data.message;
                    this.getAppointments();
                    this.hideAddAppointmentModal();
                }

            }).catch(error => {
                console.log(error);
            });

        },
        confirmDelete(id) {
            this.appointmentIdToDelete = id;
            $('#confirmDeletetModal').modal('show');
        },
        deleteAppointment() {
            let url = '../delete_appointment/' + this.appointmentIdToDelete;
            this.axios.delete(url).then(response => {
                if (response.data.success) {
                    this.successMessage = response.data.message;
                    this.getAppointments();
                    $('#confirmDeletetModal').modal('hide');
                    this.appointmentIdToDelete = null;
                }

            }).catch(error => {
                console.log(error);
            });


        }
    },
    created() {
        this.getAppointments();
    },
    mounted() {
        new flatpickr('#flatpickr-date', {
            //allowInput: true,
            minDate: 'today'
        })

        new flatpickr('#flatpickr-time', {
            enableTime: true,
            noCalendar: true,
            dateFormat: "H:i"
        })

        const modal = document.getElementById('saveAppointmentModal');

        modal.addEventListener('hide.bs.modal', () => {
            this.appointmentId = '';
            this.appointmentDate = '';
            this.appointmentTime = '';
            this.appointmentDoctor = '';
            this.appointmentLocation = '';
            this.appointmentTitle = '';
            //this.saveAppointmentModalTitle = '';
        })
    }

} 
</script>