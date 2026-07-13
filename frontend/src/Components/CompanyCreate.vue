<template>
  <div class="container mt-5" style="max-width: 560px;">
    <div class="border rounded-3 shadow-sm p-4">
      <h2 class="mb-4 text-center">Post a Placement Drive</h2>

      <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label for="job_title" class="form-label">Job Title</label>
          <input type="text" class="form-control" id="job_title" v-model="formData.job_title" placeholder="e.g. Software Engineer" required />
        </div>

        <div class="mb-3">
          <label for="job_description" class="form-label">Job Description</label>
          <textarea class="form-control" id="job_description" v-model="formData.job_description" rows="3" placeholder="Describe the role, responsibilities..." required></textarea>
        </div>

        <div class="mb-3">
          <label for="eligibility_branch" class="form-label">Eligible Branches</label>
          <input type="text" class="form-control" id="eligibility_branch" v-model="formData.eligibility_branch" placeholder="e.g. CSE, IT, ECE" required />
        </div>

        <div class="row">
          <div class="col mb-3">
            <label for="min_cgpa" class="form-label">Min CGPA</label>
            <input type="number" step="0.01" min="0" max="10" class="form-control" id="min_cgpa" v-model="formData.min_cgpa" placeholder="e.g. 7.5" required />
          </div>
          <div class="col mb-3">
            <label for="passing_year" class="form-label">Passing Year</label>
            <input type="number" class="form-control" id="passing_year" v-model="formData.passing_year" placeholder="e.g. 2025" required />
          </div>
        </div>

        <div class="row">
          <div class="col mb-3">
            <label for="package" class="form-label">Package (LPA)</label>
            <input type="number" step="0.1" class="form-control" id="package" v-model="formData.package" placeholder="e.g. 12" required />
          </div>
          <div class="col mb-3">
            <label for="location" class="form-label">Location</label>
            <input type="text" class="form-control" id="location" v-model="formData.location" placeholder="e.g. Bangalore" required />
          </div>
        </div>

        <div class="row">
          <div class="col mb-3">
            <label for="application_deadline" class="form-label">Application Deadline</label>
            <input type="date" class="form-control" id="application_deadline" v-model="formData.application_deadline" required />
          </div>
          <div class="col mb-3">
            <label for="drive_date" class="form-label">Drive Date</label>
            <input type="date" class="form-control" id="drive_date" v-model="formData.drive_date" required />
          </div>
        </div>

        <button type="submit" class="btn btn-primary w-100" :disabled="isSubmitting">
          <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
          Post Drive
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
  name: "CompanyCreateDrive",
  data() {
    return {
      formData: {
        job_title: "", job_description: "", eligibility_branch: "",
        min_cgpa: "", passing_year: "", package: "", location: "",
        application_deadline: "", drive_date: "",
      },
      isSubmitting: false,
      successMessage: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleSubmit() {
      this.isSubmitting = true;
      this.successMessage = "";
      this.errorMessage = "";
      const companyId = localStorage.getItem("company_id");
      const token = localStorage.getItem("token");
      try {
        const res = await axios.post("http://localhost:5000/api/company/drives", {
          ...this.formData,
          company_id: parseInt(companyId),
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.successMessage = res.data.message || "Drive posted successfully!";
        setTimeout(() => { this.$router.push("/company_drives"); }, 2000);
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/");
        } else {
          this.errorMessage = err.response?.data?.message || "Failed to create drive. Please try again.";
        }
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>
