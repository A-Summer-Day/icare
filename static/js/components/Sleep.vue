<template>
    <div class="">
        <div class="d-flex align-items-center justify-content-between">
            <h2>Sleep History</h2>
            <button type="button" class="btn btn-primary" @click="openSaveSleepModal(null)"> Add Sleep</button>
        </div>
        <div class="alert alert-success alert-dismissible fade show" role="alert" v-if="successMessage">
            {{ successMessage }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div class="alert alert-danger alert-dismissible fade show" role="alert" v-if="errorMessage">
            {{ errorMessage }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>

        <div class="row justify-content-center mt-5">
            <div class="col-12">
                <!-- <primvevue-timeline align="bottom" layout="horizontal" :value="displayedSleepRecords">
                    <template #content="slotProps">
                        <h5 class="mb-2">{{ formatDate(slotProps.item.date, 'L') }}</h5>
                        <p>({{ slotProps.item.total_hours }} hours)</p>
                    </template>
                </primvevue-timeline> -->
                <primvevue-timeline :value="displayedSleepRecords">
                    <template #opposite="slotProps">
                        <small class="p-text-secondary">{{ formatDate(slotProps.item.date, 'L') }}</small>
                    </template>
                    <template #content="slotProps">
                        {{ slotProps.item.total_hours }} hours
                    </template>
                </primvevue-timeline>
                <!-- Pagination controls -->
                <nav aria-label="Sleep Records Pagination" class="mt-3">
                    <ul class="pagination justify-content-center mt-4">
                        <li class="page-item" :class="{ disabled: currentPage === 1 }">
                            <a class="page-link" href="#" @click="prevPage">Previous</a>
                        </li>

                        <li v-for="page in totalPages" :key="page" class="page-item"
                            :class="{ active: currentPage === page }">
                            <a class="page-link" href="#" @click="goToPage(page)">{{ page }}</a>
                        </li>

                        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                            <a class="page-link" href="#" @click="nextPage">Next</a>
                        </li>
                    </ul>
                </nav>
                <!-- <div class="row row-cols-1 row-cols-md-3 g-4">
                    <div v-for="record in displayedRecords" :key="record.id" class="col">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Sleep Record {{ record.id }}</h5>
                                <p class="card-text">Date: {{ record.date }}</p>
                                <p class="card-text">Duration: {{ record.total_hours }} hours</p>
                                <p class="card-text">Quality: {{ record.quality }}</p>
                                <p class="card-text">Notes: {{ record.notes }}</p>
                            </div>
                        </div>
                    </div>
                </div>
                <nav aria-label="Sleep Records Pagination">
                    <ul class="pagination justify-content-center mt-4">
                        <li class="page-item" :class="{ disabled: currentPage === 1 }">
                            <a class="page-link" href="#" @click="prevPage">Previous</a>
                        </li>

                        <li v-for="page in totalPages" :key="page" class="page-item"
                            :class="{ active: currentPage === page }">
                            <a class="page-link" href="#" @click="goToPage(page)">{{ page }}</a>
                        </li>

                        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                            <a class="page-link" href="#" @click="nextPage">Next</a>
                        </li>
                    </ul>
                </nav> -->
                <!-- <full-calendar :options="calendarOptions">
                    <template v-slot:eventContent='arg'>
                        <div v-if="arg.event.extendedProps.source == 'mood'">
                            <div class="capitalize">
                                {{ arg.event.title }}
                                <i v-if="arg.event.extendedProps.mood == 'HAPPY'" class='bx bx-happy-beaming'></i>
                                <i v-if="arg.event.extendedProps.mood == 'SAD'" class='bx bx-sad'></i>
                                <i v-if="arg.event.extendedProps.mood == 'NEUTRAL'" class='bx bx-meh'></i>
                            </div>
                        </div>
                        <div v-else-if="arg.event.extendedProps.source == 'sleep'">
                            <div class="capitalize" data-bs-toggle="modal" data-bs-target="#sleepDetails">
                                {{ arg.event.title }}
                            </div>
                        </div>
                        <div v-else-if="arg.event.extendedProps.source == 'cycle'">
                            <i class='bx bx-droplet'></i><i class='bx bx-droplet'></i><i class='bx bx-droplet'></i>
                        </div>
                        <div v-else-if="arg.event.extendedProps.source == 'intercourse'">
                            <i class='bx bx-heart'></i><i class='bx bx-heart'></i><i class='bx bx-heart'></i>
                        </div>
                    </template>
                </full-calendar> -->
                <!-- <div class="modal fade" id="sleepDetails" tabindex="-1" aria-labelledby="sleepDetailsLabel"
                    aria-hidden="true">
                    <div class="modal-dialog modal-sm" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="sleepDetailsLabel">{{ sleepDetails.title }}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                                </button>
                            </div>
                            <div class="modal-body">
                                <p>Doctor: <span v-if="sleepDetails.doctor">{{ sleepDetails.doctor
                                }}</span><span v-else>N/A</span></p>
                                <p>Location: <a v-if="sleepDetails.location"
                                        :href="`https://maps.google.com/?q=${sleepDetails.location}`" target="_blank">
                                        {{ sleepDetails.location }}</a><span v-else>N/A</span></p>

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
                </div> -->
                <div class="modal fade" id="saveSleepModal" tabindex="-1" aria-labelledby="" aria-hidden="true">
                    <div class="modal-dialog" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="">{{ saveSleepModalTitle }}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                                </button>
                            </div>
                            <div class="modal-body">
                                <form id="saveSleepForm">
                                    <div class="row mb-3">
                                        <label for="flatpickr-date" class="col-sm-3 col-form-label">Date</label>
                                        <div class="col-sm-9">
                                            <input type="text" class="form-control" placeholder="YYYY-MM-DD" name="date"
                                                v-model="sleepDate" id="flatpickr-date" />

                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <label for="sleepTitle" class="col-sm-3 col-form-label">Sleep</label>
                                        <div class="col-sm-9">
                                            <input type="text" class="form-control" id="sleepTitle" name="title"
                                                v-model="sleepTitle">
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <label for="sleepDoctor" class="col-sm-3 col-form-label">Doctor</label>
                                        <div class="col-sm-9">
                                            <input type="text" class="form-control" id="sleepDoctor" name="doctor"
                                                v-model="sleepDoctor">
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <label for="sleepLocation" class="col-sm-3 col-form-label">Location</label>
                                        <div class="col-sm-9">
                                            <input type="text" class="form-control" id="sleepLocation" name="location"
                                                v-model="sleepLocation">
                                        </div>
                                    </div>
                                </form>

                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="button" class="btn btn-primary" @click="saveSleep">Save</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template> 
<script>
import moment from 'moment'

export default {
    name: 'Sleep',
    props: [],
    data: function () {
        return {
            sleepId: '',
            sleepDate: '',
            sleepQuality: '',
            sleepTotalHours: '',
            sleepNotes: '',
            sleep: [],
            sleepPerPage: 5,
            currentPage: 1,
            successMessage: '',
            errorMessage: '',
        };
    },
    computed: {
        saveSleepModalTitle() {
            return this.sleepId ? 'Edit Sleep' : 'Add Sleep';
        },
        totalPages() {
            return Math.ceil(this.sleep.length / this.sleepPerPage);
        },
        displayedSleepRecords() {
            const startIndex = (this.currentPage - 1) * this.sleepPerPage;
            const endIndex = startIndex + this.sleepPerPage;
            return this.sleep.slice(startIndex, endIndex);
        },
    },
    watch: {
        sleep: {
            handler: function (newValue, oldValue) {

            },
            deep: true,
            immediate: true
        },

    },
    methods: {
        formatDate(date, format) {
            return moment(date).format(format);
        },


        openSaveSleepModal(sleep = null) {
            console.log(sleep);
            if (sleep != null) {
                this.sleepId = sleep.id;
                this.sleepDate = sleep.date;
                this.sleepQuality = sleep.quality;
                this.sleepTotalHours = sleep.total_hours;
                this.sleepNotes = sleep.notes;
            }

            $('#saveSleepModal').modal('show');
        },
        hideSaveSleepModal() {
            $('#saveSleepForm')[0].reset();
            $('#saveSleepModal').modal('hide');
        },
        getSleep() {
            let url = '../get_sleep/';
            this.axios.get(url).then(response => {
                this.sleep = response.data.sleep;

            }).catch(error => {
                console.log(error);
            });
        },
        saveSleep() {
            console.log('sleep added');
            let url = '../save_sleep/';
            let data = new FormData()
            data.append('date', this.sleepDate)
            data.append('title', this.sleepTitle)
            data.append('doctor', this.sleepDoctor)
            data.append('location', this.sleepLocation)
            this.axios.post(url, data).then(response => {
                console.log(response.data)
                if (response.data.success) {
                    this.successMessage = response.data.message;
                    this.getSleep();
                    $('#saveSleepModal').modal('hide');
                    $('#saveSleepForm')[0].reset();
                }

            }).catch(error => {
                console.log(error);
            });

        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        goToPage(page) {
            this.currentPage = page;
        },
    },
    created() {
        this.getSleep();
    },
    mounted() {
        new flatpickr('#flatpickr-date', {
            minDate: 'today'
        })

        const modal = document.getElementById('saveSleepModal');

        modal.addEventListener('hide.bs.modal', () => {
            this.sleepId = '';
            this.sleepDate = '';
            this.sleepQuality = '';
            this.sleepTotalHours = '';
            this.sleepNotes = '';
        })
    }

} 
</script>