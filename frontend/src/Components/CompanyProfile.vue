<template>
  <div class="container mt-5" style="max-width: 500px;">
    <div class="border rounded-3 shadow-sm p-4">
      <h2 class="mb-4 text-center">Complete Your Profile</h2>

      <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label for="company_name" class="form-label">Company Name</label>
          <input type="text" class="form-control" id="company_name" v-model="formData.name" placeholder="e.g. Infosys" required />
        </div>

        <div class="mb-3">
          <label for="hr_name" class="form-label">HR Name</label>
          <input type="text" class="form-control" id="hr_name" v-model="formData.hr_name" placeholder="e.g. John Doe" required />
        </div>

        <div class="mb-3">
          <label for="phone" class="form-label">Phone</label>
          <input type="tel" class="form-control" id="phone" v-model="formData.contact" placeholder="e.g. 9876543210" required />
        </div>

        <div class="mb-3">
          <label for="description" class="form-label">Description</label>
          <input type="text" class="form-control" id="description" v-model="formData.description" placeholder="e.g. we are india's best semiconductor producer..." />
        </div>

        <div class="mb-3">
          <label for="website" class="form-label">Website URL</label>
          <input type="url" class="form-control" id="website" v-model="formData.web" placeholder="https://myweb.google.com/..." />
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
  name: "CompanyProfile",
  data() {
    return {
      formData: { name: "", hr_name: "", web: "", description: "", contact: "" },
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
      const token = localStorage.getItem("token");
      try {
        const res = await axios.post(`http://localhost:5000/api/company_profile/${userId}`, this.formData, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        localStorage.setItem("company_id", res.data.company_id);
        this.successMessage = res.data.message || "Profile saved successfully!";
        setTimeout(() => { this.$router.push("/company_dashboard"); }, 2000);
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/");
        } else {
          this.errorMessage = err.response?.data?.message || "Failed to save profile. Please try again.";
        }
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>
