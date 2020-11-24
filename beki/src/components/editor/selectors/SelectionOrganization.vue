<template>
  <cross-reference-selection
    :label="label"
    :value="value"
    @input="updateValue"
    @open-edit="openModalEdit"
    @open-new="openModalNew" required>

    <generic-edit-modal
      endpoint="api/organization"
      :is-visible="isModalVisible"
      @close="closeModal">

      <template slot-scope="{ commit, discard }">
        <modal-organization
          :commit="commit"
          :discard="discard">
        </modal-organization>
      </template>
    </generic-edit-modal>
  </cross-reference-selection>
</template>

<script>
import CrossReferenceSelection from '../../utility/CrossReferenceSelection'
import GenericEditModal from '../GenericEditModal'
import ModalOrganization from '../modal_forms/ModalOrganization.vue'
// import { newOrganization } from '../../../store/common'

export default {
  name: "SelectionOrganization",
  components: { CrossReferenceSelection, GenericEditModal, ModalOrganization },
  props: {
    value: Object,
    label: {
      type: String,
      default: "Organisation:"
    }
  },
  data() {
    return {
      isModalVisible: false,
    }
  },
  methods: {
    openModalEdit() {
      this.isModalVisible = true;
    },
    closeModal(selectedObj) {
      this.isModalVisible = false;

      if(selectedObj !== null) {
        this.bubbleInput(selectedObj);
      }
    },
    updateValue(obj) {
      this.$emit("input", obj);
    }
  }
}
</script>

<style>
</style>
