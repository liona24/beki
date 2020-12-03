<template>
  <div class="box">
    <status-indicator :status="overlayStatus">
      <h4 class="title is-4">{{ title }}</h4>
    </status-indicator>
    <slot>
    </slot>
    <nav class="level">
      <div class="level-left"></div>
      <div class="level-right">
        <div class="level-item">
          <button class="button is-dark" @click="commit" :disabled="isCommitting">Speichern</button>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import StatusIndicator from '../../../utility/StatusIndicator.vue'

export default {
  components: { StatusIndicator },
  name: "SimpleEditorLayout",
  props: {
    commitAction: String,
    title: String,
  },
  data() {
    return {
      isCommitting: false
    };
  },
  computed: {
    ...mapGetters(['overlayStatus'])
  },
  methods: {
    commit() {
      if (this.isCommitting) {
        return false;
      }

      this.isCommitting = true;
      this.$store.dispatch(this.commitAction)
        .then(wasUpdated => {
          if (wasUpdated) {
            this.$buefy.snackbar.open("Gespeichert.");
          }
          this.$store.dispatch("back_overlay", { discard: !wasUpdated });
        }, errors => {
          errors.forEach(err => {
            this.$buefy.snackbar.open({
              duration: 6000,
              message: `${err.target ? err.target : 'Fehler'}: ${err.msg}`,
              type: 'is-danger',
              queue: false
            })
          })
        })
        .finally(() => this.isCommitting = false);
    },
  }
}
</script>

<style>

</style>
