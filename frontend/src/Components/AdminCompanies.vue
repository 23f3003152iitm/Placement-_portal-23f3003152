<template>
  <div class="container mt-5" style="max-width: 1100px;">
    <h2 class="mb-4 text-center">Company Management</h2>

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
      <p class="mt-2 text-muted">Loading companies...</p>
    </div>

    <div v-else>
      <div v-if="companies.length === 0" class="text-center text-muted py-5">
        No companies found.
      </div>

      <div v-else class="border rounded-3 shadow-sm p-3 overflow-auto">
        <table class="table table-bordered table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>#</th>
              <th>Company</th>
              <th>HR Name</th>
              <th>HR Contact</th>
              <th>Website</th>
              <th>Email</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(company, index) in companies" :key="company.id">
              <td>{{ index + 1 }}</td>
              <td>{{ company.company_name }}</td>
              <td>{{ company.hr_name }}</td>
              <td>{{ company.hr_contact }}</td>
              <td>
                <a :href="company.website" target="_blank" rel="noopener">{{ company.website }}</a>
              </td>
              <td>{{ company.email }}</td>
              <td>
                <span :class="statusBadge(company.approval_status)">
                  {{ company.approval_status }}
                </span>
              </td>
              <td>
                <div class="d-flex flex-wrap gap-1">
                  <button class="btn btn-sm btn-success" :disabled="actionLoading === company.id" @click="approveCompany(company.id)">Approve</button>
                  <button class="btn btn-sm btn-warning" :disabled="actionLoading === company.id" @click="rejectCompany(company.id)">Reject</button>
                  <button class="btn btn-sm btn-secondary" :disabled="actionLoading === company.id" @click="blacklistCompany(company.id)">Blacklist</button>
                  <button class="btn btn-sm btn-danger" :disabled="actionLoading === company.id" @click="deleteCompany(company.id)">Delete</button>
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
  name: "AdminCompanies",
  data() {
    return {
      companies: [],
      isLoading: false,
      actionLoading: null,
      successMessage: "",
      errorMessage: "",
    };
  },
  async mounted() {
    await this.fetchCompanies();
  },
  methods: {
    async fetchCompanies() {
      this.isLoading = true;
      this.errorMessage = "";
      try {
        const res = await axios.get("http://localhost:5000/api/admin/companies");
        this.companies = res.data;
      } catch (err) {
        this.errorMessage = "Failed to load companies.";
      } finally {
        this.isLoading = false;
      }
    },

    async approveCompany(id) { await this.performAction(id, "put", `/api/admin/company/${id}/approve`); },
    async rejectCompany(id) { await this.performAction(id, "put", `/api/admin/company/${id}/reject`); },
    async blacklistCompany(id) { await this.performAction(id, "put", `/api/admin/company/${id}/blacklist`); },
    async deleteCompany(id) {
      if (!confirm("Are you sure you want to delete this company?")) return;
      await this.performAction(id, "delete", `/api/admin/company/${id}`);
    },

    async performAction(id, method, endpoint) {
      this.actionLoading = id;
      this.successMessage = "";
      this.errorMessage = "";
      try {
        const res = await axios[method](`http://localhost:5000${endpoint}`);
        this.successMessage = res.data.message || "Action completed.";
        await this.fetchCompanies();
      } catch (err) {
        this.errorMessage = err.response?.data?.message || "Action failed. Please try again.";
      } finally {
        this.actionLoading = null;
      }
    },

    statusBadge(status) {
      const map = {
        Approved: "badge bg-success",
        Rejected: "badge bg-danger",
        Pending: "badge bg-warning text-dark",
      };
      return map[status] || "badge bg-secondary";
    },
  },
};
</script>
