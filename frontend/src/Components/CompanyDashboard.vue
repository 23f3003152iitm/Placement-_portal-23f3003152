<template>
  <div class="container mt-5" style="max-width: 860px;">
    <h2 class="mb-4 text-center">Company Dashboard</h2>

    <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

    <div v-if="isLoading" class="text-center py-5">
      <span class="spinner-border text-primary"></span>
      <p class="mt-2 text-muted">Loading dashboard...</p>
    </div>

    <div v-else>
      <!-- Welcome Banner -->
      <div class="d-flex align-items-center justify-content-between bg-primary bg-opacity-10 border border-primary border-opacity-25 rounded-3 p-4 mb-4">
        <div>
          <div class="fs-5 fw-bold">{{ stats.company_name }}</div>
          <div class="text-muted small mt-1">Company Portal</div>
        </div>
        <span :class="statusBadge(stats.approval_status)">{{ stats.approval_status }}</span>
      </div>

      <div v-if="stats.approval_status !== 'Approved'" class="alert alert-warning">
        ⚠️ Your company is not yet approved by the admin. You cannot create placement drives until approved.
      </div>

      <!-- Stats Cards -->
      <div class="row g-4 mb-4">
        <div class="col-sm-6">
          <div class="border rounded-3 shadow-sm p-4 text-center h-100">
            <div class="d-inline-flex align-items-center justify-content-center rounded-circle bg-primary bg-opacity-10 mb-3" style="width:52px;height:52px;">
              <i class="bi bi-briefcase-fill text-primary fs-5"></i>
            </div>
            <div class="fs-2 fw-bold">{{ stats.drive_count }}</div>
            <div class="text-muted small mb-3">Placement Drives Posted</div>
            <router-link to="/company_drives" class="small text-decoration-none">View All →</router-link>
          </div>
        </div>

        <div class="col-sm-6">
          <div class="border rounded-3 shadow-sm p-4 text-center h-100">
            <div class="d-inline-flex align-items-center justify-content-center rounded-circle bg-success bg-opacity-10 mb-3" style="width:52px;height:52px;">
              <i class="bi bi-file-earmark-person-fill text-success fs-5"></i>
            </div>
            <div class="fs-2 fw-bold">{{ stats.application_count }}</div>
            <div class="text-muted small mb-3">Total Applications Received</div>
            <router-link to="/company_applications" class="small text-decoration-none">Manage →</router-link>
          </div>
        </div>
      </div>

      <!-- Quick Nav -->
      <h5 class="mb-3 text-muted">Quick Links</h5>
      <div class="d-flex flex-wrap gap-2">
        <router-link to="/company_drives" class="btn btn-outline-primary">My Drives</router-link>
        <router-link to="/company_create" class="btn btn-outline-success">Post New Drive</router-link>
        <router-link to="/company_edit" class="btn btn-outline-success">Edit</router-link>
        <router-link to="/company_profile" class="btn btn-outline-success">Create Profile</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CompanyDashboard",
  data() {
    return {
      stats: { company_name: "", approval_status: "", drive_count: 0, application_count: 0 },
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
      const companyId = localStorage.getItem("company_id");
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get(`http://localhost:5000/api/company/dashboard/${companyId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.stats = res.data;
      } catch (err) {
          if (err.response?.status === 401) {
            localStorage.clear()
            this.$router.push("/")   // token expired → back to login
          } else {
            console.error(err);
            this.errorMessage = "Failed to load dashboard.";
          }
      } finally {
        this.isLoading = false;
      }
    },

    statusBadge(status) {
      const map = { Approved: "badge bg-success fs-6", Rejected: "badge bg-danger fs-6", Pending: "badge bg-warning text-dark fs-6" };
      return map[status] || "badge bg-secondary fs-6";
    },
  },
};
</script>
