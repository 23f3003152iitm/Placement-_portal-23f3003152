<template>
  <div class="container mt-5" style="max-width: 1100px;">
    <h2 class="mb-4 text-center">Placement Drive Management</h2>

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
        No placement drives found.
      </div>

      <div v-else class="border rounded-3 shadow-sm p-3 overflow-auto">
        <table class="table table-bordered table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>#</th>
              <th>Job Title</th>
              <th>Company</th>
              <th>Min CGPA</th>
              <th>Deadline</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(drive, index) in drives" :key="drive.id">
              <td>{{ index + 1 }}</td>
              <td>{{ drive.job_title }}</td>
              <td>{{ drive.company_name }}</td>
              <td>{{ drive.min_cgpa }}</td>
              <td>{{ formatDate(drive.deadline) }}</td>
              <td>
                <span :class="statusBadge(drive.status)">{{ drive.status }}</span>
              </td>
              <td>
                <div class="d-flex flex-wrap gap-1">
                  <button class="btn btn-sm btn-success" :disabled="actionLoading === drive.id" @click="approveDrive(drive.id)">Approve</button>
                  <button class="btn btn-sm btn-warning" :disabled="actionLoading === drive.id" @click="rejectDrive(drive.id)">Reject</button>
                  <button class="btn btn-sm btn-secondary" :disabled="actionLoading === drive.id" @click="closeDrive(drive.id)">
                    <span v-if="actionLoading === drive.id" class="spinner-border spinner-border-sm me-1"></span>
                    Close
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
  name: "AdminDrives",
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
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get("http://localhost:5000/api/admin/drives", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.drives = res.data;
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/login");
        } else {
          this.errorMessage = "Failed to load placement drives.";
        }
      } finally {
        this.isLoading = false;
      }
    },

    async approveDrive(id) { await this.performAction(id, "put", `/api/admin/drive/${id}/approve`); },
    async rejectDrive(id) { await this.performAction(id, "put", `/api/admin/drive/${id}/reject`); },
    async closeDrive(id) { await this.performAction(id, "put", `/api/admin/drive/${id}/close`); },

    async performAction(id, method, endpoint) {
      this.actionLoading = id;
      this.successMessage = "";
      this.errorMessage = "";
      try {
        const res = await axios[method](`http://localhost:5000${endpoint}`);
        this.successMessage = res.data.message || "Action completed.";
        await this.fetchDrives();
      } catch (err) {
        this.errorMessage = err.response?.data?.message || "Action failed. Please try again.";
      } finally {
        this.actionLoading = null;
      }
    },

    formatDate(dateStr) {
      if (!dateStr) return "N/A";
      return new Date(dateStr).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });
    },

    statusBadge(status) {
      const map = {
        Approved: "badge bg-success",
        Rejected: "badge bg-danger",
        Pending: "badge bg-warning text-dark",
        Closed: "badge bg-secondary",
      };
      return map[status] || "badge bg-secondary";
    },
  },
};
</script>
