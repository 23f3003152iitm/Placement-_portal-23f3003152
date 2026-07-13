<template>
  <div class="container mt-5" style="max-width: 500px;">
    <h2 class="mb-4 text-center">Register</h2>

    <!-- Alerts -->
    <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
    <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

    <form @submit.prevent="handleRegister">
            <div class="mb-3">
        <label for="name" class="form-label">Name</label>
        <input
          type="text"
          class="form-control"
          id="name"
          v-model="formData.name"
          required
        />
      </div>

      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          class="form-control"
          id="email"
          v-model="formData.email"
          required
        />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Role</label>
        <input
          type="text"
          class="form-control"
          id="password" 
          v-model="formData.role"
          required
        />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
          type="password"
          class="form-control"
          id="password"
          v-model="formData.password"
          required
        />
      </div>

      <button type="submit" class="btn btn-primary w-100" :disabled="isSubmitting">
        <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
        Register
      </button>
    </form>

    <p class="mt-3 text-center">
      Already have an account? <router-link to="/login">Login here</router-link>
    </p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Register",
  data() {
    return {
      formData: {
        email: "",
        password: "",
        name: "",
        role: "",
      },
      isSubmitting: false,
      successMessage: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleRegister() {
      this.isSubmitting = true;
      this.successMessage = "";
      this.errorMessage = "";

      try {
        const res = await axios.post("http://localhost:5000/api/register", this.formData);
        this.successMessage = res.data.message || "Registered successfully!";
        this.formData.email = "";
        this.formData.password = "";

        // Optional: redirect to login after 2 sec
        setTimeout(() => {
          this.$router.push("/");
        }, 2000);

      } catch (err) {
        if (err.response && err.response.data && err.response.data.message) {
          this.errorMessage = err.response.data.message;
        } else {
          this.errorMessage = "Registration failed. Please try again.";
        }
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>

<style scoped>
.container {
  border: 1px solid #ddd;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>