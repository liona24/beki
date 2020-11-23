<template>
  <cross-reference-many-selection
    :label="label"
    :value="value"
    @input="bubbleInput"
    @open-modal="openModal" required>

    <generic-edit-modal
      endpoint="api/inspection_standard"
      :is-visible="isModalVisible"
      @close="closeModal">

      <template slot-scope="{ commit, discard }">
        <modal-inspection-standard
          :initial="value"
          :commit="commit"
          :discard="discard">
        </modal-inspection-standard>
      </template>
    </generic-edit-modal>
  </cross-reference-many-selection>
</template>

<script>
import CrossReferenceManySelection from '../../utility/CrossReferenceManySelection'
import GenericEditModal from '../GenericEditModal'
import ModalInspectionStandard from '../modal_forms/ModalInspectionStandard'

export default {
  name: "ManySelectionInspectionStandard",
  components: { CrossReferenceManySelection, GenericEditModal, ModalInspectionStandard },
  props: {
    value: Array,
    label: {
      type: String,
      default: "Prüfkriterium:"
    }
  },
  data() {
    return {
      isModalVisible: false,
    }
  },
  methods: {
    openModal() {
      this.isModalVisible = true;
    },
    closeModal(selectedObj) {
      this.isModalVisible = false;

      if(selectedObj !== null) {
        this.bubbleInput(selectedObj);
      }
    },
    bubbleInput(obj) {
      this.$emit("input", obj);
    }
  }
}
</script>

<style>

</style>
