<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card shadow p-4" style="width: 400px;">
      <h3 class="text-center mb-4">Login</h3>

      <!-- Error -->
      <div v-if="error" class="alert alert-danger text-center">
        {{ error }}
      </div>

      <!-- Email -->
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input
          v-model="email"
          type="email"
          class="form-control"
          placeholder="Enter email"
        />
      </div>

      <!-- Password -->
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input
          v-model="password"
          type="password"
          class="form-control"
          placeholder="Enter password"
        />
      </div>

      <!-- Button -->
      <button class="btn btn-primary w-100" @click="handleLogin">
        Login
      </button>
      <h5 class="text-center mt-3">
        New user ? <router-link to="/register">Register here</router-link>
      </h5>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useUserStore } from "../stores/user"
import { useRouter } from "vue-router"

const email = ref("")
const password = ref("")
const error = ref("")

const store = useUserStore()
const router = useRouter()



// async arrow function to handle login
const handleLogin = async () => {
  try {
    const user = await store.login(email.value, password.value)
    
   
    if (user.role === "admin") {
      router.push("/admin_dash")
    } 


    
    else if (user.role === "company") {
      router.push("/company_dash")
    } 


    else if (user.role === "student") {
      const studentId = localStorage.getItem("student_id")
      if (studentId) {
        router.push("/student_dash")        // existing student → dashboard
      } else {
        router.push("/student_profile")     // new student → complete profile
      }
    }

    else {
      error.value = "Unknown role"
    }

  } catch (e) {
    error.value = e.message
  }
}


</script>