<template>
    <div class="">
        <div class="d-flex align-items-center justify-content-between">
            <h2>Contacts</h2>
            <button type="button" class="btn btn-primary" @click="openAddContactModal(null)"> Add Contact</button>
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
                <primvevue-data-table id="contactTable" :value="contacts" paginator :rows="10" stripedRows tableStyle="min-width: 50rem;">
                    <template #empty> <p class="text-center">No contacts found. </p></template>
                    <template #loading> <div class="text-center">Loading contacts data. Please wait. </div></template>
                    <!-- <primvevue-column field="first_name" header="First Name" sortable></primvevue-column>
                    <primvevue-column field="last_name" header="Last Name" sortable></primvevue-column> -->
                    <primvevue-column header="Full Name" sortable>
                        <template #body="slotProps">
                            {{ slotProps.data.last_name ? slotProps.data.first_name + ' ' + slotProps.data.last_name : slotProps.data.first_name }}
                        </template>
                    </primvevue-column>
                    <primvevue-column field="email" header="Email" sortable></primvevue-column>
                    <primvevue-column field="phone_number" header="Phone Number" sortable></primvevue-column>
                    <primvevue-column field="address" header="Address" sortable></primvevue-column>
                    <primvevue-column field="notes" header="Notes" sortable></primvevue-column>
                    <primvevue-column field="actions" header="Actions">
                        <template #body="{ data }">
                            <div class="d-flex">
                                <a class="dropdown-item edit-btn" href="javascript:void(0);"
                                    @click="openAddContactModal(data)">
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
            </div>
        </div>
        <div class="modal fade" id="saveContactModal" tabindex="-1" aria-labelledby="saveContactModalLabel"
            aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="">Add a contact</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                        </button>
                    </div>
                    <div class="modal-body">
                        <form id="saveContactForm">
                            <div class="row mb-3">
                                <label for="contactFirstName" class="col-sm-3 col-form-label">First Name</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" id="contactFirstName"
                                        name="first_name" v-model="contactFirstName" />
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="contactLastName" class="col-sm-3 col-form-label">Last Name</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" id="contactLastName"
                                        name="last_name" v-model="contactLastName" />
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="contactEmail" class="col-sm-3 col-form-label">Email</label>
                                <div class="col-sm-9">
                                    <input type="email" class="form-control" id="contactEmail"
                                        name="email" placeholder="name@example.com" v-model="contactEmail">
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="contactPhoneNumbe" class="col-sm-3 col-form-label">Phone Number</label>
                                <div class="col-sm-9">
                                    <input type="tel" class="form-control" id="contactPhoneNumbe"
                                        name="phone_number" v-model="contactPhoneNumber" />
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="contactAddress" class="col-sm-3 col-form-label">Address</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" id="contactAddress" name="address"
                                        v-model="contactAddress">
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="contactTitle" class="col-sm-3 col-form-label">Notes</label>
                                <div class="col-sm-9">
                                    <textarea class="form-control" id="contactNotes" name="notes"
                                        v-model="contactNotes"></textarea>
                                </div>
                            </div>
                        </form>

                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" @click="saveContact">Save</button>
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
                        <button type="button" class="btn btn-danger" @click="deleteContact">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template> 
<script>

import moment from 'moment'

export default {
    name: 'Contacts',
    props: [],
    data: function () {
        return {
            contactId: '',
            contactFirstName: '',
            contactLastName: '',
            contactEmail: '',
            contactPhoneNumber: '',
            contactAddress: '',
            contactNotes: '',
            contactIdToDelete: null,
            contactToEdit: null,
            contacts: [],
            successMessage: '',
            errorMessage: '',
            
        };
    },
    computed: {

    },
    methods: {
        formatDate(date, format) {
            return moment(date).format(format);
        },
        formatTime(time, format) {
            return moment(time, 'HH:mm:ss').format(format);
        },
        openAddContactModal(contact = null) {
            console.log(contact);
            if (contact != null) {
                this.contactId = contact.id;
                this.contactFirstName = contact.first_name;
                this.contactLastName = contact.last_name;
                this.contactEmail = contact.email;
                this.contactPhoneNumber = contact.phone_number;
                this.contactAddress = contact.address;
                this.contactNotes = contact.notes;
            }

            $('#saveContactModal').modal('show');
        },
        hideAddContactModal() {
            $('#saveContactForm')[0].reset();
            $('#saveContactModal').modal('hide');
        },
        getContacts() {
            let url = '../get_contacts/';
            this.axios.get(url).then(response => {
                this.contacts = response.data.contacts;


            }).catch(error => {
                console.log(error);
            });
        },
        saveContact() {
            let url = this.contactId ? '../update_contact/' : '../save_contact/';
            let data = new FormData()
            if (this.contactId) {
                data.append('id', this.contactId);
            }
            data.append('first_name', this.contactFirstName)
            data.append('last_name', this.contactLastName);
            data.append('email', this.contactEmail);
            data.append('phone_number', this.contactPhoneNumber);
            data.append('address', this.contactAddress);
            data.append('notes', this.contactNotes);

            this.axios.post(url, data).then(response => {
                console.log(response.data)
                if (response.data.success) {
                    this.successMessage = response.data.message;
                    this.getContacts();
                    this.hideAddContactModal();
                }

            }).catch(error => {
                console.log(error);
            });

        },
        confirmDelete(id) {
            console.log(id);
            this.contactIdToDelete = id;
            $('#confirmDeletetModal').modal('show');
        },
        deleteContact() {
            let url = '../delete_contact/' + this.contactIdToDelete;
            this.axios.delete(url).then(response => {
                if (response.data.success) {
                    this.successMessage = response.data.message;
                    this.getContacts();
                    $('#confirmDeletetModal').modal('hide');
                    this.contactIdToDelete = null;
                }

            }).catch(error => {
                console.log(error);
            });
        }
    },
    created() {
        this.getContacts();
    },
    mounted() {
        const modal = document.getElementById('saveContactModal');

        modal.addEventListener('hide.bs.modal', () => {
            this.contactId = '';
            this.contactFirstName = '';
            this.contactLastName = '';
            this.contactEmail = '';
            this.contactPhoneNumber = '';
            this.contactAddress = '';
            this.contactNotes = ''
        })


    }

} 
</script>
<style>
.p-datatable-wrapper {
    overflow: unset !important;
}
</style>