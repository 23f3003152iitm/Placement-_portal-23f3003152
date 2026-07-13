<template>
  <div class="container mt-5" style="max-width: 960px;">
    <h2 class="mb-4 text-center">Available Placement Drives</h2>

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
        No approved drives available right now.
      </div>

      <div class="row g-4" v-else>
        <div class="col-md-6" v-for="drive in drives" :key="drive.id">
          <div class="border rounded-3 shadow-sm p-4 h-100">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div>
                <div class="fw-bold fs-6">{{ drive.job_title }}</div>
                <div class="text-muted small mt-1">{{ drive.company_name }}</div>
              </div>
              <span class="badge bg-success">Open</span>
            </div>

            <div class="d-flex flex-column gap-2 mb-3">
              <div class="d-flex justify-content-between small text-secondary">
                <span>📦 Package</span><span>{{ drive.package }} LPA</span>
              </div>
              <div class="d-flex justify-content-between small text-secondary">
                <span>📍 Location</span><span>{{ drive.location }}</span>
              </div>
              <div class="d-flex justify-content-between small text-secondary">
                <span>🎓 Min CGPA</span><span>{{ drive.min_cgpa }}</span>
              </div>
              <div class="d-flex justify-content-between small text-secondary">
                <span>⏰ Deadline</span><span>{{ formatDate(drive.deadline) }}</span>
              </div>
            </div>
              <div class="d-flex justify-content-between small text-secondary">
                <span> 📦📦 Inhand</span><span>{{  (drive.package * 0.8).toFixed(2)  }}</span>
              </div>
            </div>

            <button
              class="btn btn-primary w-100"
              :disabled="applyingId === drive.id"
              @click="applyForDrive(drive.id)"
            >
              <span v-if="applyingId === drive.id" class="spinner-border spinner-border-sm me-2"></span>
              Apply Now
            </button>
          </div>
        </div>
      </div>
    </div>
  <!-- </div> -->
</template>

<script>
import axios from "axios";

export default {
  name: "StudentDrives",
  data() {
    return {
      drives: [],
      isLoading: false,
      applyingId: null,
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
        const res = await axios.get("http://localhost:5000/api/student/drives", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.drives = res.data;
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/");
        } else {
          this.errorMessage = "Failed to load drives.";
        }
      } finally {
        this.isLoading = false;
      }
    },

    async applyForDrive(driveId) {
      this.applyingId = driveId;
      this.successMessage = "";
      this.errorMessage = "";
      const studentId = localStorage.getItem("student_id");
      const token = localStorage.getItem("token");
      try {
        const res = await axios.post("http://localhost:5000/api/student/apply", {
          student_id: parseInt(studentId),
          drive_id: driveId,
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.successMessage = res.data.message || "Applied successfully!";
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/login");
        } else {
          this.errorMessage = err.response?.data?.message || "Failed to apply. Please try again.";
        }
      } finally {
        this.applyingId = null;
      }
    },

    formatDate(dateStr) {
      if (!dateStr) return "N/A";
      return new Date(dateStr).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });
    },
  },
};
</script>
