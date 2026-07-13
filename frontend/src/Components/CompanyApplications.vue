<template>
  <div class="container mt-5" style="max-width: 1050px;">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Drive Applications</h2>
      <router-link to="/company/drives" class="btn btn-outline-secondary btn-sm">← Back to Drives</router-link>
    </div>

    <div v-if="successMessage" class="alert alert-success alert-dismissible">
      {{ successMessage }}
      <button type="button" class="btn-close" @click="successMessage = ''"></button>
    </div>
    <div v-if="errorMessage" class="alert alert-danger alert-dismissible">
      {{ errorMessage }}
      <button type="button" class="btn-close" @click="errorMessage = ''"></button>
    </div>

    <div v-if="isLoading" class="text-center py-5">
      <span class="spinner-border text-primary"></span>
      <p class="mt-2 text-muted">Loading applications...</p>
    </div>

    <div v-else>
      <div v-if="applications.length === 0" class="text-center text-muted py-5">
        No applications received for this drive yet.
      </div>

      <div v-else class="border rounded-3 shadow-sm p-3 overflow-auto">
        <table class="table table-bordered table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>#</th><th>Student</th><th>Email</th><th>Branch</th>
              <th>CGPA</th><th>Status</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(app, index) in applications" :key="app.application_id">
              <td>{{ index + 1 }}</td>
              <td>{{ app.student_name }}</td>
              <td>{{ app.student_email }}</td>
              <td>{{ app.branch }}</td>
              <td>{{ app.cgpa }}</td>
              <td><span :class="statusBadge(app.status)">{{ app.status }}</span></td>
              <td>
                <div class="d-flex flex-wrap gap-1">
                  <button class="btn btn-sm btn-outline-primary" @click="openStatusModal(app)">Update Status</button>
                  <button class="btn btn-sm btn-outline-warning" @click="openInterviewModal(app)">Schedule Interview</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Update Status Modal -->
    <div v-if="statusModal.show" class="modal d-block" style="background:rgba(0,0,0,0.45);" @click.self="closeStatusModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content p-2">
          <div class="modal-header border-0">
            <h5 class="modal-title">Update Status — {{ statusModal.studentName }}</h5>
            <button type="button" class="btn-close" @click="closeStatusModal"></button>
          </div>
          <div class="modal-body">
            <div v-if="statusModal.successMessage" class="alert alert-success">{{ statusModal.successMessage }}</div>
            <div v-if="statusModal.errorMessage" class="alert alert-danger">{{ statusModal.errorMessage }}</div>
            <div class="mb-3">
              <label class="form-label">Status</label>
              <select class="form-select" v-model="statusModal.status">
                <option value="Applied">Applied</option>
                <option value="Shortlisted">Shortlisted</option>
                <option value="Interview Scheduled">Interview Scheduled</option>
                <option value="Selected">Selected</option>
                <option value="Rejected">Rejected</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label">Remarks (optional)</label>
              <textarea class="form-control" v-model="statusModal.remarks" rows="2" placeholder="Any remarks for the student..."></textarea>
            </div>
          </div>
          <div class="modal-footer border-0 gap-2">
            <button class="btn btn-primary w-100" @click="submitStatusUpdate" :disabled="statusModal.isSubmitting">
              <span v-if="statusModal.isSubmitting" class="spinner-border spinner-border-sm me-2"></span>Save
            </button>
            <button class="btn btn-outline-secondary w-100" @click="closeStatusModal">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Schedule Interview Modal -->
    <div v-if="interviewModal.show" class="modal d-block" style="background:rgba(0,0,0,0.45);" @click.self="closeInterviewModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content p-2">
          <div class="modal-header border-0">
            <h5 class="modal-title">Schedule Interview — {{ interviewModal.studentName }}</h5>
            <button type="button" class="btn-close" @click="closeInterviewModal"></button>
          </div>
          <div class="modal-body">
            <div v-if="interviewModal.successMessage" class="alert alert-success">{{ interviewModal.successMessage }}</div>
            <div v-if="interviewModal.errorMessage" class="alert alert-danger">{{ interviewModal.errorMessage }}</div>
            <div class="mb-3">
              <label class="form-label">Interview Date & Time</label>
              <input type="datetime-local" class="form-control" v-model="interviewModal.interview_date" />
            </div>
          </div>
          <div class="modal-footer border-0 gap-2">
            <button class="btn btn-warning w-100" @click="submitScheduleInterview" :disabled="interviewModal.isSubmitting || !interviewModal.interview_date">
              <span v-if="interviewModal.isSubmitting" class="spinner-border spinner-border-sm me-2"></span>Schedule
            </button>
            <button class="btn btn-outline-secondary w-100" @click="closeInterviewModal">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CompanyApplications",
  data() {
    return {
      applications: [],
      isLoading: false,
      successMessage: "",
      errorMessage: "",
      statusModal: { show: false, applicationId: null, studentName: "", status: "Applied", remarks: "", isSubmitting: false, successMessage: "", errorMessage: "" },
      interviewModal: { show: false, applicationId: null, studentName: "", interview_date: "", isSubmitting: false, successMessage: "", errorMessage: "" },
    };
  },
  async mounted() {
    await this.fetchApplications();
  },
  methods: {
    async fetchApplications() {
      this.isLoading = true;
      this.errorMessage = "";
      const driveId = this.$route.params.id;
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get(`http://localhost:5000/api/company/applications/${driveId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.applications = res.data;
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/");
        } else {
          this.errorMessage = "Failed to load applications.";
        }
      } finally {
        this.isLoading = false;
      }
    },

    openStatusModal(app) {
      this.statusModal = { show: true, applicationId: app.application_id, studentName: app.student_name, status: app.status, remarks: "", isSubmitting: false, successMessage: "", errorMessage: "" };
    },
    closeStatusModal() { this.statusModal.show = false; },

    async submitStatusUpdate() {
      this.statusModal.isSubmitting = true;
      this.statusModal.successMessage = "";
      this.statusModal.errorMessage = "";
      const token = localStorage.getItem("token");
      try {
        const res = await axios.put(`http://localhost:5000/api/company/application/${this.statusModal.applicationId}/status`, { status: this.statusModal.status, remarks: this.statusModal.remarks }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.statusModal.successMessage = res.data.message || "Status updated.";
        await this.fetchApplications();
        setTimeout(() => this.closeStatusModal(), 1500);
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/");
        } else {
          this.statusModal.errorMessage = err.response?.data?.message || "Failed to update status.";
        }
      } finally {
        this.statusModal.isSubmitting = false;
      }
    },

    openInterviewModal(app) {
      this.interviewModal = { show: true, applicationId: app.application_id, studentName: app.student_name, interview_date: "", isSubmitting: false, successMessage: "", errorMessage: "" };
    },
    closeInterviewModal() { this.interviewModal.show = false; },

    async submitScheduleInterview() {
      this.interviewModal.isSubmitting = true;
      this.interviewModal.successMessage = "";
      this.interviewModal.errorMessage = "";
      const formatted = this.interviewModal.interview_date.replace("T", " ") + ":00";
      const token = localStorage.getItem("token");
      try {
        const res = await axios.put(`http://localhost:5000/api/company/application/${this.interviewModal.applicationId}/interview`, { interview_date: formatted }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.interviewModal.successMessage = res.data.message || "Interview scheduled.";
        await this.fetchApplications();
        setTimeout(() => this.closeInterviewModal(), 1500);
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/");
        } else {
          this.interviewModal.errorMessage = err.response?.data?.message || "Failed to schedule interview.";
        }
      } finally {
        this.interviewModal.isSubmitting = false;
      }
    },

    statusBadge(status) {
      const map = { Applied: "badge bg-primary", Shortlisted: "badge bg-info text-dark", "Interview Scheduled": "badge bg-warning text-dark", Selected: "badge bg-success", Rejected: "badge bg-danger" };
      return map[status] || "badge bg-secondary";
    },
  },
};
</script>
