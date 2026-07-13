<template>
  <div class="container mt-5" style="max-width: 860px;">
    <h2 class="mb-4 text-center">My Applications</h2>

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
        You haven't applied to any drives yet.<br />
        <router-link to="/student/drives" class="btn btn-primary mt-3">Browse Drives</router-link>
      </div>

      <div v-else class="border rounded-3 shadow-sm p-3 overflow-auto">
        <table class="table table-bordered table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>#</th><th>Job Title</th><th>Company</th>
              <th>Status</th><th>Interview Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(app, index) in applications" :key="app.application_id">
              <td>{{ index + 1 }}</td>
              <td>{{ app.job_title }}</td>
              <td>{{ app.company_name }}</td>
              <td><span :class="statusBadge(app.status)">{{ app.status }}</span></td>
              <td>{{ formatDate(app.interview_date) }}</td>
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
  name: "StudentApplications",
  data() {
    return {
      applications: [],
      isLoading: false,
      errorMessage: "",
    };
  },
  async mounted() {
    await this.fetchApplications();
  },
  methods: {
    async fetchApplications() {
      this.isLoading = true;
      this.errorMessage = "";
      const token = localStorage.getItem("token");
      const studentId = localStorage.getItem("student_id");
      try {
        const res = await axios.get(`http://localhost:5000/api/student/applications/${studentId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.applications = res.data;
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/login");
        } else {
          this.errorMessage = "Failed to load applications.";
        }
      } finally {
        this.isLoading = false;
      }
    },

    formatDate(dateStr) {
      if (!dateStr) return "Not scheduled";
      return new Date(dateStr).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });
    },

    statusBadge(status) {
      const map = { Applied: "badge bg-primary", Shortlisted: "badge bg-info text-dark", Selected: "badge bg-success", Rejected: "badge bg-danger" };
      return map[status] || "badge bg-secondary";
    },
  },
};
</script>
