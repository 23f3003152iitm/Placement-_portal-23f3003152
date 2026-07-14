<template>
  <div class="container mt-5" style="max-width: 960px;">
    <h2 class="mb-4 text-center">Admin Dashboard</h2>

    <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

    <div v-if="isLoading" class="text-center py-5">
      <span class="spinner-border text-primary"></span>
      <p class="mt-2 text-muted">Loading dashboard...</p>
    </div>

    <div v-else class="row g-4">
      <div class="col-md-3 col-sm-6">
        <div class="border rounded-3 shadow-sm p-4 text-center h-100">
          <div class="d-inline-flex align-items-center justify-content-center rounded-circle bg-primary bg-opacity-10 mb-3" style="width:52px;height:52px;">
            <i class="bi bi-mortarboard-fill text-primary fs-5"></i>
          </div>
          <div class="fs-2 fw-bold">{{ stats.student_count }}</div>
          <div class="text-muted small mb-3">Total Students</div>
          <router-link to="/admin_students" class="small text-decoration-none">View All →</router-link>
        </div>
      </div>

      <div class="col-md-3 col-sm-6">
        <div class="border rounded-3 shadow-sm p-4 text-center h-100">
          <div class="d-inline-flex align-items-center justify-content-center rounded-circle bg-success bg-opacity-10 mb-3" style="width:52px;height:52px;">
            <i class="bi bi-building-fill text-success fs-5"></i>
          </div>
          <div class="fs-2 fw-bold">{{ stats.company_count }}</div>
          <div class="text-muted small mb-3">Total Companies</div>
          <router-link to="/admin_companies" class="small text-decoration-none">View All →</router-link>
        </div>
      </div>

      <div class="col-md-3 col-sm-6">
        <div class="border rounded-3 shadow-sm p-4 text-center h-100">
          <div class="d-inline-flex align-items-center justify-content-center rounded-circle bg-warning bg-opacity-10 mb-3" style="width:52px;height:52px;">
            <i class="bi bi-briefcase-fill text-warning fs-5"></i>
          </div>
          <div class="fs-2 fw-bold">{{ stats.drive_count }}</div>
          <div class="text-muted small mb-3">Placement Drives</div>
          <router-link to="/admin_drives" class="small text-decoration-none">View All →</router-link>
        </div>
      </div>

      <div class="col-md-3 col-sm-6">
        <div class="border rounded-3 shadow-sm p-4 text-center h-100">
          <div class="d-inline-flex align-items-center justify-content-center rounded-circle bg-danger bg-opacity-10 mb-3" style="width:52px;height:52px;">
            <i class="bi bi-file-earmark-text-fill text-danger fs-5"></i>
          </div>
          <div class="fs-2 fw-bold">{{ stats.application_count }}</div>
          <div class="text-muted small mb-3">Applications</div>
          <router-link to="/admin_applications" class="small text-decoration-none">View All →</router-link>
        </div>
      </div>
    </div>

    <div class="mt-5">
      <h5 class="mb-3 text-muted">Quick Navigation</h5>
      <div class="d-flex flex-wrap gap-2">
        <router-link to="/admin_students" class="btn btn-outline-primary">Students</router-link>
        <router-link to="/admin_companies" class="btn btn-outline-success">Companies</router-link>
        <router-link to="/admin_drives" class="btn btn-outline-warning">Drives</router-link>
        <router-link to="/admin_applications" class="btn btn-outline-danger">Applications</router-link>
        <router-link to="/Admin_searchs" class="btn btn-outline-secondary">Search</router-link>
      </div>
    </div> 
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdminDashboard",
  data() {
    return {
      stats: { student_count: 0, company_count: 0, drive_count: 0, application_count: 0 },
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
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get("http://localhost:5000/api/admin/dashboard", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.stats = res.data;
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/login");
        } else {
          this.errorMessage = "Failed to load dashboard data.";
        }
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>
