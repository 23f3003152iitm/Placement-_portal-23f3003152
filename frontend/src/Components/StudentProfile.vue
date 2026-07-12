<template>
  <div class="container mt-5" style="max-width: 500px;">
    <div class="border rounded-3 shadow-sm p-4">
      <h2 class="mb-4 text-center">Complete Your Profile</h2>

      <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label for="branch" class="form-label">Branch</label>
          <input type="text" class="form-control" id="branch" v-model="formData.branch" placeholder="e.g. Computer Science" required />
        </div>

        <div class="mb-3">
          <label for="cgpa" class="form-label">CGPA</label>
          <input type="number" step="0.01" min="0" max="10" class="form-control" id="cgpa" v-model="formData.cgpa" placeholder="e.g. 8.5" required />
        </div>

        <div class="mb-3">
          <label for="phone" class="form-label">Phone</label>
          <input type="tel" class="form-control" id="phone" v-model="formData.phone" placeholder="e.g. 9876543210" required />
        </div>

        <div class="mb-3">
          <label for="passing_year" class="form-label">Passing Year</label>
          <input type="number" class="form-control" id="passing_year" v-model="formData.passing_year" placeholder="e.g. 2025" required />
        </div>

        <div class="mb-3">
          <label for="skills" class="form-label">Skills</label>
          <input type="text" class="form-control" id="skills" v-model="formData.skills" placeholder="e.g. Python, React, SQL" />
        </div>

        <div class="mb-3">
          <label for="resume" class="form-label">Resume URL</label>
          <input type="url" class="form-control" id="resume" v-model="formData.resume" placeholder="https://drive.google.com/..." />
        </div>

        <button type="submit" class="btn btn-primary w-100" :disabled="isSubmitting">
          <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
          Save Profile
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "StudentProfileRegister",
  data() {
    return {
      formData: { branch: "", cgpa: "", phone: "", passing_year: "", skills: "", resume: "" },
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
      const userId = localStorage.getItem("id");
      try {
        const res = await axios.post(`http://localhost:5000/api/student_profile/${userId}`, this.formData);
        localStorage.setItem("student_id", res.data.student_id);
        this.successMessage = res.data.message || "Profile saved successfully!";
        setTimeout(() => { this.$router.push("/student_dashboard"); }, 2000);
      } catch (err) {
        this.errorMessage = err.response?.data?.message || "Failed to save profile. Please try again.";
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>
