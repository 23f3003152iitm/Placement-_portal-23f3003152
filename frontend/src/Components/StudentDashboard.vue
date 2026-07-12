<template>
  <div class="container mt-5" style="max-width: 860px;">
    <h2 class="mb-4 text-center">Student Dashboard</h2>

    <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

    <div v-if="isLoading" class="text-center py-5">
      <span class="spinner-border text-primary"></span>
      <p class="mt-2 text-muted">Loading dashboard...</p>
    </div>

    <div v-else>
      <!-- Welcome Banner -->
      <div class="d-flex align-items-center justify-content-between bg-primary bg-opacity-10 border border-primary border-opacity-25 rounded-3 p-4 mb-4">
        <div>
          <div class="fs-5 fw-bold">Welcome, {{ stats.student_name }} 👋</div>
          <div class="text-muted small mt-1">{{ stats.branch }}</div>
        </div>
        <span class="badge bg-primary fs-6">CGPA: {{ stats.cgpa }}</span>
      </div>

      <!-- Stats Cards -->
      <div class="row g-4 mb-4">
        <div class="col-sm-6">
          <div class="border rounded-3 shadow-sm p-4 text-center h-100">
            <div class="d-inline-flex align-items-center justify-content-center rounded-circle bg-primary bg-opacity-10 mb-3" style="width:52px;height:52px;">
              <i class="bi bi-file-earmark-check-fill text-primary fs-5"></i>
            </div>
            <div class="fs-2 fw-bold">{{ stats.applied_count }}</div>
            <div class="text-muted small mb-3">Applications Submitted</div>
            <router-link to="/student_applications" class="small text-decoration-none">View →</router-link>
          </div>
        </div>

        <div class="col-sm-6">
          <div class="border rounded-3 shadow-sm p-4 text-center h-100">
            <div class="d-inline-flex align-items-center justify-content-center rounded-circle bg-success bg-opacity-10 mb-3" style="width:52px;height:52px;">
              <i class="bi bi-briefcase-fill text-success fs-5"></i>
            </div>
            <div class="fs-2 fw-bold">{{ stats.approved_drives }}</div>
            <div class="text-muted small mb-3">Open Drives Available</div>
            <router-link to="/student_drives" class="small text-decoration-none">Explore →</router-link>
          </div>
        </div>
      </div>

      <!-- Quick Nav -->
      <h5 class="mb-3 text-muted">Quick Links</h5>
      <div class="d-flex flex-wrap gap-2">
        <router-link to="/student_drives" class="btn btn-outline-primary">Browse Drives</router-link>
        <router-link to="/student_applications" class="btn btn-outline-secondary">My Applications</router-link>
        <router-link to="/student_history" class="btn btn-outline-success">Placement History</router-link>
        <router-link to="/student_profile" class="btn btn-outline-warning">My Profile</router-link>
        <router-link to="/student_edit" class="btn btn-outline-warning">Edit Profile</router-link>
        <button @click="exportCSV" class="btn btn-outline-dark">📁 Export My Applications</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "StudentDashboard",
  data() {
    return {
      stats: { student_name: "", branch: "", cgpa: "", applied_count: 0, approved_drives: 0 },
      isLoading: false,
      errorMessage: "",
    };
  },
  async mounted() {
    await this.fetchDashboard();
  },
  methods: {
    async fetchDashboard() {
      this.isLoading = true;
      this.errorMessage = "";
      const studentId = localStorage.getItem("student_id");
      try {
        const res = await axios.get(`http://localhost:5000/api/student/dashboard/${studentId}`);
        this.stats = res.data;
      } catch (err) {
        this.errorMessage = "Failed to load dashboard.";
      } finally {
        this.isLoading = false;
      }
    },
    async exportCSV() {
  const studentId = localStorage.getItem("student_id")
  try {
    const res = await axios.post(`http://localhost:5000/api/student/export/${studentId}`)
    alert(res.data.message)
  } catch (err) {
    alert("Export failed. Please try again.")
  }
}
  },
};
</script>
