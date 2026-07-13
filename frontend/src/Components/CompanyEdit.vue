<template>
  <div class="container mt-5" style="max-width: 560px;">
    <div class="border rounded-3 shadow-sm p-4">
      <h2 class="mb-4 text-center">Edit Placement Drive</h2>

      <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

      <div v-if="isLoading" class="text-center py-5">
        <span class="spinner-border text-primary"></span>
        <p class="mt-2 text-muted">Loading drive details...</p>
      </div>

      <form v-else @submit.prevent="handleUpdate">
        <div class="mb-3">
          <label for="job_title" class="form-label">Job Title</label>
          <input type="text" class="form-control" id="job_title" v-model="formData.job_title" required />
        </div>

        <div class="mb-3">
          <label for="job_description" class="form-label">Job Description</label>
          <textarea class="form-control" id="job_description" v-model="formData.job_description" rows="3" required></textarea>
        </div>

        <div class="row">
          <div class="col mb-3">
            <label for="min_cgpa" class="form-label">Min CGPA</label>
            <input type="number" step="0.01" min="0" max="10" class="form-control" id="min_cgpa" v-model="formData.min_cgpa" required />
          </div>
          <div class="col mb-3">
            <label for="package" class="form-label">Package (LPA)</label>
            <input type="number" step="0.1" class="form-control" id="package" v-model="formData.package" required />
          </div>
        </div>

        <div class="mb-3">
          <label for="location" class="form-label">Location</label>
          <input type="text" class="form-control" id="location" v-model="formData.location" required />
        </div>

        <button type="submit" class="btn btn-primary w-100" :disabled="isSubmitting">
          <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
          Update Drive
        </button>

        <p class="mt-3 text-center">
          <router-link to="/company/drives">← Back to My Drives</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CompanyEditDrive",
  data() {
    return {
      formData: { job_title: "", job_description: "", min_cgpa: "", package: "", location: "" },
      isLoading: false,
      isSubmitting: false,
      successMessage: "",
      errorMessage: "",
    };
  },
  async mounted() {
    await this.loadDrive();
  },
  methods: {
    async loadDrive() {
      this.isLoading = true;
      this.errorMessage = "";
      const driveId = this.$route.params.id;
      const companyId = localStorage.getItem("company_id");
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get(`http://localhost:5000/api/company/drives/${companyId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const drive = res.data.find((d) => d.id === parseInt(driveId));
        if (drive) { this.formData.job_title = drive.job_title || ""; }
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/login");
        } else {
          this.errorMessage = "Failed to load drive details.";
        }
      } finally {
        this.isLoading = false;
      }
    },

    async handleUpdate() {
      this.isSubmitting = true;
      this.successMessage = "";
      this.errorMessage = "";
      const token = localStorage.getItem("token");
      const driveId = this.$route.params.id;
      try {
        const res = await axios.put(`http://localhost:5000/api/company/drive/${driveId}`, this.formData, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.successMessage = res.data.message || "Drive updated successfully!";
        setTimeout(() => { this.$router.push("/company/drives"); }, 2000);
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/");
        } else {
          this.errorMessage = err.response?.data?.message || "Update failed. Please try again.";
        }
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>
