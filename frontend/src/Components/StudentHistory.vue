<template>
  <div class="container mt-5" style="max-width: 860px;">
    <h2 class="mb-4 text-center">Placement History</h2>

    <div v-if="errorMessage" class="alert alert-danger alert-dismissible">
      {{ errorMessage }}
      <button type="button" class="btn-close" @click="errorMessage = ''"></button>
    </div>

    <div v-if="isLoading" class="text-center py-5">
      <span class="spinner-border text-primary"></span>
      <p class="mt-2 text-muted">Loading history...</p>
    </div>

    <div v-else>
      <div v-if="history.length === 0" class="text-center text-muted py-5">
        No placement history yet. Keep applying!<br />
        <router-link to="/student/drives" class="btn btn-primary mt-3">Browse Drives</router-link>
      </div>

      <div class="row g-4" v-else>
        <div class="col-md-6" v-for="(item, index) in history" :key="index">
          <div class="border border-success rounded-3 shadow-sm p-4 h-100 bg-success bg-opacity-10">
            <span class="badge bg-success mb-2">🎉 Selected</span>
            <div class="fw-bold fs-6">{{ item.job_title }}</div>
            <div class="text-muted small mt-1 mb-3">{{ item.company_name }}</div>

            <div class="d-flex flex-column gap-2">
              <div class="d-flex justify-content-between small">
                <span class="text-muted">💰 Package</span>
                <span class="fw-semibold text-success">{{ item.package }} LPA</span>
              </div>
              <div class="d-flex justify-content-between small">
                <span class="text-muted">📅 Selected On</span>
                <span class="fw-semibold text-success">{{ formatDate(item.selected_date) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "StudentHistory",
  data() {
    return {
      history: [],
      isLoading: false,
      errorMessage: "",
    };
  },
  async mounted() {
    await this.fetchHistory();
  },
  methods: {
    async fetchHistory() {
      this.isLoading = true;
      this.errorMessage = "";
      const studentId = localStorage.getItem("student_id");
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get(`http://localhost:5000/api/student/history/${studentId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.history = res.data;
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/login");
        } else {
          this.errorMessage = "Failed to load placement history.";
        }
      } finally {
        this.isLoading = false;
      }
    },

    formatDate(dateStr) {
      if (!dateStr) return "N/A";
      return new Date(dateStr).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });
    },
  },
};
</script>
