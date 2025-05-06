import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    resources: [],
    loading: false,
    error: null
  },
  mutations: {
    setResources(state, resources) {
      state.resources = resources
    },
    setLoading(state, status) {
      state.loading = status
    },
    setError(state, error) {
      state.error = error
    },
    addResource(state, resource) {
      state.resources.push(resource)
    }
  },
  actions: {
    // Fetch all learning resources
    async fetchResources({ commit }) {
      commit('setLoading', true)
      commit('setError', null)
      
      try {
        const response = await axios.get('/api/resources/')
        commit('setResources', response.data)
      } catch (error) {
        commit('setError', 'Failed to load resources. Please try again.')
        console.error('Error fetching resources:', error)
      } finally {
        commit('setLoading', false)
      }
    },
    
    // Create a new learning resource
    async createResource({ commit }, resource) {
      commit('setLoading', true)
      commit('setError', null)
      
      try {
        const response = await axios.post('/api/resources/', resource)
        commit('addResource', response.data)
        return response.data
      } catch (error) {
        commit('setError', 'Failed to create resource. Please try again.')
        console.error('Error creating resource:', error)
        throw error
      } finally {
        commit('setLoading', false)
      }
    }
  }
})