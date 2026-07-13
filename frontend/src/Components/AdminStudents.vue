<template>
  <div class="container mt-5" style="max-width: 1100px;">
    <h2 class="mb-4 text-center">Student Management</h2>

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
      <p class="mt-2 text-muted">Loading students...</p>
    </div>

    <div v-else>
      <div v-if="students.length === 0" class="text-center text-muted py-5">
        No students found.
      </div>

      <div v-else class="border rounded-3 shadow-sm p-3 overflow-auto">
        <table class="table table-bordered table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>#</th><th>Name</th><th>Email</th><th>Branch</th>
              <th>CGPA</th><th>Passing Year</th><th>Phone</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(student, index) in students" :key="student.id">
              <td>{{ index + 1 }}</td>
              <td>{{ student.name }}</td>
              <td>{{ student.email }}</td>
              <td>{{ student.branch }}</td>
              <td>{{ student.cgpa }}</td>
              <td>{{ student.passing_year }}</td>
              <td>{{ student.phone }}</td>
              <td>
                <div class="d-flex flex-wrap gap-1">
                  <button class="btn btn-sm btn-secondary" :disabled="actionLoading === student.id" @click="blacklistStudent(student.id)">
                    <span v-if="actionLoading === student.id" class="spinner-border spinner-border-sm me-1"></span>
                    Blacklist
                  </button>
                  <button class="btn btn-sm btn-danger" :disabled="actionLoading === student.id" @click="deleteStudent(student.id)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdminStudents",
  data() {
    return {
      students: [],
      isLoading: false,
      actionLoading: null,
      successMessage: "",
      errorMessage: "",
    };
  },
  async mounted() {
    await this.fetchStudents();
  },
  methods: {
    async fetchStudents() {
      this.isLoading = true;
      this.errorMessage = "";
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get("http://localhost:5000/api/admin/students", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.students = res.data;
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/login");
        } else {
          this.errorMessage = "Failed to load students.";
        }
      } finally {
        this.isLoading = false;
      }
    },

    async blacklistStudent(id) { await this.performAction(id, "put", `/api/admin/student/${id}/blacklist`); },
    async deleteStudent(id) {
      if (!confirm("Are you sure you want to delete this student?")) return;
      await this.performAction(id, "delete", `/api/admin/student/${id}`);
    },

    async performAction(id, method, endpoint) {
      this.actionLoading = id;
      this.successMessage = "";
      this.errorMessage = "";
      const token = localStorage.getItem("token");
      try {
        const res = await axios[method](`http://localhost:5000${endpoint}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.successMessage = res.data.message || "Action completed.";
        await this.fetchStudents();
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/");
        } else {
          this.errorMessage = err.response?.data?.message || "Action failed. Please try again.";
        }
      } finally {
        this.actionLoading = null;
      }
    },
  },
};
</script>
