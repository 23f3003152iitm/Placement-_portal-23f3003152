<template>
  <div class="container mt-5" style="max-width: 960px;">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">My Placement Drives</h2>
      <router-link to="/company/drives/create" class="btn btn-primary">+ Post New Drive</router-link>
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
      <p class="mt-2 text-muted">Loading drives...</p>
    </div>

    <div v-else>
      <div v-if="drives.length === 0" class="text-center text-muted py-5">
        No drives posted yet.<br />
        <router-link to="/company/drives/create" class="btn btn-primary mt-3">Post Your First Drive</router-link>
      </div>

      <div v-else class="border rounded-3 shadow-sm p-3 overflow-auto">
        <table class="table table-bordered table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>#</th><th>Job Title</th><th>Status</th>
              <th>Deadline</th><th>Drive Date</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(drive, index) in drives" :key="drive.id">
              <td>{{ index + 1 }}</td>
              <td>{{ drive.job_title }}</td>
              <td><span :class="statusBadge(drive.status)">{{ drive.status }}</span></td>
              <td>{{ formatDate(drive.deadline) }}</td>
              <td>{{ formatDate(drive.drive_date) }}</td>
              <td>
                <div class="d-flex flex-wrap gap-1">
                  <button class="btn btn-sm btn-outline-primary" @click="viewApplications(drive.id)">Applications</button>
                  <button class="btn btn-sm btn-warning" @click="editDrive(drive.id)">Edit</button>
                  <button class="btn btn-sm btn-danger" :disabled="actionLoading === drive.id" @click="deleteDrive(drive.id)">
                    <span v-if="actionLoading === drive.id" class="spinner-border spinner-border-sm me-1"></span>
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CompanyDrives",
  data() {
    return {
      drives: [],
      isLoading: false,
      actionLoading: null,
      successMessage: "",
      errorMessage: "",
    };
  },
  async mounted() {
    await this.fetchDrives();
  },
  methods: {
    async fetchDrives() {
      this.isLoading = true;
      this.errorMessage = "";
      const companyId = localStorage.getItem("company_id");
      try {
        const res = await axios.get(`http://localhost:5000/api/company/drives/${companyId}`);
        this.drives = res.data;
      } catch (err) {
        this.errorMessage = "Failed to load drives.";
      } finally {
        this.isLoading = false;
      }
    },

    async deleteDrive(id) {
      if (!confirm("Are you sure you want to delete this drive?")) return;
      this.actionLoading = id;
      this.successMessage = "";
      this.errorMessage = "";
      try {
        const res = await axios.delete(`http://localhost:5000/api/company/drive/${id}`);
        this.successMessage = res.data.message || "Drive deleted.";
        await this.fetchDrives();
      } catch (err) {
        this.errorMessage = err.response?.data?.message || "Failed to delete drive.";
      } finally {
        this.actionLoading = null;
      }
    },

    viewApplications(driveId) { this.$router.push(`/company/drives/${driveId}/applications`); },
    editDrive(driveId) { this.$router.push(`/company/drives/${driveId}/edit`); },

    formatDate(dateStr) {
      if (!dateStr) return "N/A";
      return new Date(dateStr).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });
    },

    statusBadge(status) {
      const map = { Approved: "badge bg-success", Rejected: "badge bg-danger", Pending: "badge bg-warning text-dark", Closed: "badge bg-secondary" };
      return map[status] || "badge bg-secondary";
    },
  },
};
</script>
