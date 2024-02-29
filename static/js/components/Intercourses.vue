<template>
    <div class="">
        <div class="d-flex align-items-center justify-content-between">
            <h2>Intercourse History</h2>
            <button type="button" class="btn btn-primary" @click="openAddIntercourseModal(null)"> Add Intercourse</button>
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
                <primvevue-data-table id="intercourseTable" :value="intercourses" paginator :rows="10" stripedRows
                    tableStyle="min-width: 50rem;">
                    <template #empty> No intercourses found. </template>
                    <template #loading> Loading intercourses data. Please wait. </template>
                    <primvevue-column field="date" header="Date" sortable></primvevue-column>
                    <primvevue-column field="with_whom" header="With Whom" sortable :sortField="(event) => sortByFullName(event)" nullSortOrder="-1">
                        <!-- <template #body="slotProps">
                            {{ slotProps.data.with_whom.last_name ? slotProps.data.with_whom.first_name + ' ' + slotProps.data.with_whom.last_name : slotProps.data.with_whom.first_name }}
                        </template> -->
                        <template #body="{ data }">
                            {{ data.with_whom.last_name ? data.with_whom.first_name + ' ' + data.with_whom.last_name : data.with_whom.first_name }}
                        </template>
                    </primvevue-column>
                    <primvevue-column field="protection_used" header="Protection Used" sortable>
                        <template #body="slotProps">
                            {{ slotProps.data.protection_used ? 'Yes' : 'No' }}
                        </template>
                    </primvevue-column>
                    <primvevue-column field="contraception_method" header="Contraception Method"
                        sortable></primvevue-column>
                    <primvevue-column field="notes" header="Notes" sortable></primvevue-column>
                    <primvevue-column field="actions" header="Actions">
                        <template #body="{ data }">
                            <div class="d-flex">
                                <a class="dropdown-item edit-btn" href="javascript:void(0);"
                                    @click="openAddIntercourseModal(data)">
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
                <!-- <data-table ref="myDataTable" id="intercourseTable" :columns="columns" :data="intercourses"
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
        <div class="modal fade" id="saveIntercourseModal" tabindex="-1" aria-labelledby="saveIntercourseModalLabel"
            aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="">Add an intercourse</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                        </button>
                    </div>
                    <div class="modal-body">
                        <form id="saveIntercourseForm">
                            <div class="row mb-3">
                                <label for="flatpickr-date" class="col-sm-3 col-form-label">Date</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" placeholder="YYYY-MM-DD" name="date"
                                        v-model="intercourseDate" id="flatpickr-date" />

                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="intercourseProtectionUsed" class="col-sm-3 col-form-label">Protection
                                    Used</label>
                                <div class="col-sm-9">
                                    <input type="checkbox" class="form-check-input" id="intercourseProtectionUsed"
                                        name="notes" v-model="intercourseProtectionUsed">
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="intercourseContraceptionMethod" class="col-sm-3 col-form-label">Contraception
                                    Method</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" id="intercourseContraceptionMethod"
                                        name="contraception_method" v-model="intercourseContraceptionMethod" />
                                </div>
                            </div>
                            <!-- <div class="row mb-3">
                                <label for="intercourseWithWhom" class="col-sm-3 col-form-label">With Whom</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" id="intercourseWithWhom" name="with_whom"
                                        v-model="intercourseWithWhom">
                                </div>
                            </div> -->
                            <div class="row mb-3">
                                <label for="intercourseWithWhom" class="col-sm-3 col-form-label">With Whom</label>
                                <div class="col-sm-9">
                                    <primvevue-dropdown v-model="intercourseWithWhom" :options="contactOptions"
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
                                <label for="intercourseTitle" class="col-sm-3 col-form-label">Notes</label>
                                <div class="col-sm-9">
                                    <textarea class="form-control" id="intercourseNotes" name="notes"
                                        v-model="intercourseNotes"></textarea>
                                </div>
                            </div>
                        </form>

                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" @click="saveIntercourse">Save</button>
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
                        <button type="button" class="btn btn-danger" @click="deleteIntercourse">Delete</button>
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
    name: 'Intercourses',
    props: [],
    data: function () {
        return {
            intercourseId: '',
            intercourseDate: '',
            intercourseNotes: '',
            intercourseProtectionUsed: '',
            intercourseContraceptionMethod: '',
            intercourseWithWhom: '',
            intercourseIdToDelete: null,
            intercourseToEdit: null,
            intercourses: [],
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
        openAddIntercourseModal(intercourse = null) {
            console.log(intercourse);
            if (intercourse != null) {
                this.intercourseDate = intercourse.date;
                this.intercourseId = intercourse.id;
                this.intercourseContraceptionMethod = intercourse.contraception_method;
                this.intercourseProtectionUsed = intercourse.protection_used;
                this.intercourseNotes = intercourse.notes;
                this.intercourseWithWhom = intercourse.with_whom.id;
            }
            $('#saveIntercourseModal').modal('show');
        },
        hideAddIntercourseModal() {
            $('#saveIntercourseForm')[0].reset();
            $('#saveIntercourseModal').modal('hide');
        },
        getIntercourses() {
            let url = '../get_intercourses/';
            this.axios.get(url).then(response => {
                this.intercourses = response.data.intercourses;


            }).catch(error => {
                console.log(error);
            });
        },
        saveIntercourse() {
            let url = this.intercourseId ? '../update_intercourse/' : '../save_intercourse/';
            let data = new FormData()
            if (this.intercourseId) {
                data.append('id', this.intercourseId);
            }
            data.append('date', this.intercourseDate)
            data.append('with_whom', this.intercourseWithWhom);
            data.append('protection_used', this.intercourseProtectionUsed);
            data.append('contraception_method', this.intercourseContraceptionMethod);
            data.append('notes', this.intercourseNotes);
            this.axios.post(url, data).then(response => {
                console.log(response.data)
                if (response.data.success) {
                    this.successMessage = response.data.message;
                    this.getIntercourses();
                    this.hideAddIntercourseModal();
                }

            }).catch(error => {
                console.log(error);
            });

        },
        confirmDelete(id) {
            console.log(id);
            this.intercourseIdToDelete = id;
            $('#confirmDeletetModal').modal('show');
        },
        deleteIntercourse() {
            let url = '../delete_intercourse/' + this.intercourseIdToDelete;
            this.axios.delete(url).then(response => {
                if (response.data.success) {
                    this.successMessage = response.data.message;
                    this.getIntercourses();
                    $('#confirmDeletetModal').modal('hide');
                    this.intercourseIdToDelete = null;
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
        this.getIntercourses();
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

        const modal = document.getElementById('saveIntercourseModal');

        modal.addEventListener('hide.bs.modal', () => {
            this.intercourseId = '';
            this.intercourseDate = '';
            this.intercourseNotes = '';
            this.intercourseProtectionUsed = '';
            this.intercourseContraceptionMethod = '';
            this.intercourseWithWhom = '';
        })


    }

} 
</script>
<style>
.p-datatable-wrapper {
    overflow: unset !important;
}</style>