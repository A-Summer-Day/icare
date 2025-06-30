<template>
    <div class="">
        <div class="d-flex align-items-center justify-content-between">
            <h2>Physical Activities</h2>
            <button type="button" class="btn btn-primary" @click="openAddPhysicalActivityModal(null)"> Add Physical Activity</button>
        </div>


        <div class="alert alert-success alert-dismissible fade show mt-2" role="alert" v-if="successMessage">
            {{ successMessage }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div class="alert alert-danger alert-dismissible fade show mt-2" role="alert" v-if="errorMessage">
            {{ errorMessage }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div class="row justify-content-center mt-4">
            <div class="col-12">
                <primvevue-data-table id="physicalActivityTable" :value="physical_activities" paginator :rows="10" stripedRows
                    tableStyle="min-width: 50rem;">
                    <template #empty> No physical activities found. </template>
                    <template #loading> Loading physical activities data. Please wait. </template>
                    <primvevue-column field="date" header="Date" sortable></primvevue-column>
                    <primvevue-column field="activity_type" header="Activity Type" sortable>
                    </primvevue-column>
                    <!-- <primvevue-column field="activity_type" header="Activity Type" sortable :sortField="(event) => sortByFullName(event)" nullSortOrder="-1">
                        <template #body="{ data }">
                            {{ data.with_whom.last_name ? data.with_whom.first_name + ' ' + data.with_whom.last_name : data.with_whom.first_name }}
                        </template>
                    </primvevue-column> -->
                    <primvevue-column field="specific_activity" header="Specific Activity" sortable>
                    </primvevue-column> 
                    <primvevue-column field="duration_minutes" header="Duration Minutes"
                        sortable></primvevue-column>
                    <primvevue-column field="calories_burned" header="Calories Burned" sortable></primvevue-column>    
                    <primvevue-column field="notes" header="Notes" sortable></primvevue-column>
                    <primvevue-column field="actions" header="Actions">
                        <template #body="{ data }">
                            <div class="d-flex">
                                <a class="dropdown-item edit-btn" href="javascript:void(0);"
                                    @click="openAddPhysicalActivityModal(data)">
                                    <i class="bx bx-edit-alt me-1"></i>
                                </a>
                                <a class="dropdown-item delete-btn" href="javascript:void(0);"
                                    @click="confirmDelete(data.id)">
                                    <i class="bx bx-trash me-1"></i>
                                </a>
                            </div>

                        </template>
                    </primvevue-column>
                </primvevue-data-table>
                <!-- <data-table ref="myDataTable" id="physicalActivityTable" :columns="columns" :data="physical_activities"
                    class="table table-hover table-striped">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>With Whom</th>
                            <th>Protection Used</th>
                            <th>Contraception Method</th>
                            <th>Notes</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                </data-table> -->
            </div>
        </div>
        <div class="modal fade" id="savePhysicalActivityModal" tabindex="-1" aria-labelledby="savePhysicalActivityModalLabel"
            aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="">Add an physicalActivity</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                        </button>
                    </div>
                    <div class="modal-body">
                        <form id="savePhysicalActivityForm">
                            <div class="row mb-3">
                                <label for="flatpickr-date" class="col-sm-3 col-form-label">Date</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" placeholder="YYYY-MM-DD" name="date"
                                        v-model="physicalActivityDate" id="flatpickr-date" />

                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="physicalActivityProtectionUsed" class="col-sm-3 col-form-label">Protection
                                    Used</label>
                                <div class="col-sm-9">
                                    <input type="checkbox" class="form-check-input" id="physicalActivityProtectionUsed"
                                        name="notes" v-model="physicalActivityProtectionUsed">
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="physicalActivityContraceptionMethod" class="col-sm-3 col-form-label">Contraception
                                    Method</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" id="physicalActivityContraceptionMethod"
                                        name="contraception_method" v-model="physicalActivityContraceptionMethod" />
                                </div>
                            </div>
                            <!-- <div class="row mb-3">
                                <label for="physicalActivityWithWhom" class="col-sm-3 col-form-label">With Whom</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" id="physicalActivityWithWhom" name="with_whom"
                                        v-model="physicalActivityWithWhom">
                                </div>
                            </div> -->
                            <div class="row mb-3">
                                <label for="physicalActivityWithWhom" class="col-sm-3 col-form-label">With Whom</label>
                                <div class="col-sm-9">
                                    <primvevue-dropdown v-model="physicalActivityWithWhom" :options="contactOptions"
                                        optionLabel="name" optionValue="id" placeholder="Select a Contact" class="w-full md:w-14rem">

                                        <template #option="slotProps">
                                            <div class="flex align-items-center">
                                                
                                                <div>{{ slotProps.option.name }}</div>
                                            </div>
                                        </template>
                                    </primvevue-dropdown>
                                    
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="physicalActivityTitle" class="col-sm-3 col-form-label">Notes</label>
                                <div class="col-sm-9">
                                    <textarea class="form-control" id="physicalActivityNotes" name="notes"
                                        v-model="physicalActivityNotes"></textarea>
                                </div>
                            </div>
                        </form>

                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" @click="savePhysicalActivity">Save</button>
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
                        <p>Are you sure you want to delete this record?</p>

                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-danger" @click="deletePhysicalActivity">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template> 
<script>

import moment from 'moment'
import { ref } from 'vue';

export default {
    name: 'PhysicalActivities',
    props: [],
    data: function () {
        return {
            physicalActivityId: '',
            physicalActivityDate: '',
            physicalActivityNotes: '',
            physicalActivityProtectionUsed: '',
            physicalActivityContraceptionMethod: '',
            physicalActivityWithWhom: '',
            physicalActivityIdToDelete: null,
            physicalActivityToEdit: null,
            physical_activities: [],
            contacts: [],
            successMessage: '',
            errorMessage: ''
        };
    },
    computed: {
        contactOptions() {
            let options = this.contacts.map(obj => ({ ...obj, name: obj.last_name ? obj.first_name + ' ' + obj.last_name : obj.first_name }))
            console.log(options);
            return options;
        }
    },
    methods: {
        formatDate(date, format) {
            return moment(date).format(format);
        },
        formatTime(time, format) {
            return moment(time, 'HH:mm:ss').format(format);
        },
        openAddPhysicalActivityModal(physicalActivity = null) {
            console.log(physicalActivity);
            if (physicalActivity != null) {
                this.physicalActivityDate = physicalActivity.date;
                this.physicalActivityId = physicalActivity.id;
                this.physicalActivityContraceptionMethod = physicalActivity.contraception_method;
                this.physicalActivityProtectionUsed = physicalActivity.protection_used;
                this.physicalActivityNotes = physicalActivity.notes;
                this.physicalActivityWithWhom = physicalActivity.with_whom.id;
            }
            $('#savePhysicalActivityModal').modal('show');
        },
        hideAddPhysicalActivityModal() {
            $('#savePhysicalActivityForm')[0].reset();
            $('#savePhysicalActivityModal').modal('hide');
        },
        getPhysicalActivities() {
            let url = '../get_physical_activities/';
            this.axios.get(url).then(response => {
                this.physical_activities = response.data.physical_activities;


            }).catch(error => {
                console.log(error);
            });
        },
        savePhysicalActivity() {
            let url = this.physicalActivityId ? '../update_physicalActivity/' : '../save_physicalActivity/';
            let data = new FormData()
            if (this.physicalActivityId) {
                data.append('id', this.physicalActivityId);
            }
            data.append('date', this.physicalActivityDate)
            data.append('with_whom', this.physicalActivityWithWhom);
            data.append('protection_used', this.physicalActivityProtectionUsed);
            data.append('contraception_method', this.physicalActivityContraceptionMethod);
            data.append('notes', this.physicalActivityNotes);
            this.axios.post(url, data).then(response => {
                console.log(response.data)
                if (response.data.success) {
                    this.successMessage = response.data.message;
                    this.getPhysicalActivities();
                    this.hideAddPhysicalActivityModal();
                }

            }).catch(error => {
                console.log(error);
            });

        },
        confirmDelete(id) {
            console.log(id);
            this.physicalActivityIdToDelete = id;
            $('#confirmDeletetModal').modal('show');
        },
        deletePhysicalActivity() {
            let url = '../delete_physicalActivity/' + this.physicalActivityIdToDelete;
            this.axios.delete(url).then(response => {
                if (response.data.success) {
                    this.successMessage = response.data.message;
                    this.getPhysicalActivities();
                    $('#confirmDeletetModal').modal('hide');
                    this.physicalActivityIdToDelete = null;
                }

            }).catch(error => {
                console.log(error);
            });
        },
        getContacts() {
            let url = '../get_contacts/';
            this.axios.get(url).then(response => {
                this.contacts = response.data.contacts;

            }).catch(error => {
                console.log(error);
            });
        },
        sortByFullName(e) {
            return e.with_whom.last_name ? e.with_whom.first_name + ' ' + e.with_whom.last_name : e.with_whom.first_name
        }
    },
    created() {
        this.getPhysicalActivities();
        this.getContacts();
    },
    mounted() {
        new flatpickr('#flatpickr-date', {
            //minDate: 'today'
        })

        new flatpickr('#flatpickr-time', {
            enableTime: true,
            noCalendar: true,
            dateFormat: "H:i"
        })

        const modal = document.getElementById('savePhysicalActivityModal');

        modal.addEventListener('hide.bs.modal', () => {
            this.physicalActivityId = '';
            this.physicalActivityDate = '';
            this.physicalActivityNotes = '';
            this.physicalActivityProtectionUsed = '';
            this.physicalActivityContraceptionMethod = '';
            this.physicalActivityWithWhom = '';
        })


    }

} 
</script>
<style>
.p-datatable-wrapper {
    overflow: unset !important;
}</style>