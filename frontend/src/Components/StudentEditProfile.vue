<template>
  <div class="container mt-5" style="max-width: 500px;">
    <div class="border rounded-3 shadow-sm p-4">
      <h2 class="mb-4 text-center">Edit Profile</h2>

      <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

      <div v-if="isLoading" class="text-center py-5">
        <span class="spinner-border text-primary"></span>
        <p class="mt-2 text-muted">Loading profile...</p>
      </div>

      <form v-else @submit.prevent="handleUpdate">
        <div class="mb-3">
          <label for="branch" class="form-label">Branch</label>
          <input type="text" class="form-control" id="branch" v-model="formData.branch" required />
        </div>

        <div class="mb-3">
          <label for="cgpa" class="form-label">CGPA</label>
          <input type="number" step="0.01" min="0" max="10" class="form-control" id="cgpa" v-model="formData.cgpa" required />
        </div>

        <div class="mb-3">
          <label for="phone" class="form-label">Phone</label>
          <input type="tel" class="form-control" id="phone" v-model="formData.phone" required />
        </div>

        <div class="mb-3">
          <label for="passing_year" class="form-label">Passing Year</label>
          <input type="number" class="form-control" id="passing_year" v-model="formData.passing_year" required />
        </div>

        <div class="mb-3">
          <label for="skills" class="form-label">Skills</label>
          <input type="text" class="form-control" id="skills" v-model="formData.skills" placeholder="e.g. Python, React, SQL" />
        </div>

        <button type="submit" class="btn btn-primary w-100" :disabled="isSubmitting">
          <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
          Update Profile
        </button>

        <p class="mt-3 text-center">
          <router-link to="/student/dashboard">← Back to Dashboard</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "StudentEditProfile",
  data() {
    return {
      formData: { branch: "", cgpa: "", phone: "", passing_year: "", skills: "" },
      isLoading: false,
      isSubmitting: false,
      successMessage: "",
      errorMessage: "",
    };
  },
  async mounted() {
    await this.loadProfile();
  },
  methods: {
    async loadProfile() {
      this.isLoading = true;
      this.errorMessage = "";
      const studentId = localStorage.getItem("student_id");
      try {
        const res = await axios.get(`http://localhost:5000/api/student/dashboard/${studentId}`);
        this.formData.branch = res.data.branch || "";
        this.formData.cgpa = res.data.cgpa || "";
      } catch (err) {
        this.errorMessage = "Failed to load profile data.";
      } finally {
        this.isLoading = false;
      }
    },

    async handleUpdate() {
      this.isSubmitting = true;
      this.successMessage = "";
      this.errorMessage = "";
      const studentId = localStorage.getItem("student_id");
      try {
        const res = await axios.put(`http://localhost:5000/api/student/profile/${studentId}`, this.formData);
        this.successMessage = res.data.message || "Profile updated successfully!";
      } catch (err) {
        this.errorMessage = err.response?.data?.message || "Update failed. Please try again.";
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>
