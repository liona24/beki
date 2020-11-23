<template>
  <cross-reference-selection
    :label="label"
    :value="value"
    @input="bubbleInput"
    @open-modal="openModal" required>

    <generic-edit-modal
      endpoint="api/category"
      :is-visible="isModalVisible"
      @close="closeModal">

      <template slot-scope="{ commit, discard }">
        <modal-category
          :initial="value"
          :commit="commit"
          :discard="discard">
        </modal-category>
      </template>
    </generic-edit-modal>
  </cross-reference-selection>
</template>

<script>
import CrossReferenceSelection from '../../utility/CrossReferenceSelection'
import GenericEditModal from '../GenericEditModal'
import ModalCategory from '../modal_forms/ModalCategory.vue'

export default {
  name: "SelectionFacility",
  components: { CrossReferenceSelection, GenericEditModal, ModalCategory },
  props: {
    value: Object,
    label: {
      type: String,
      default: "Kategorie:"
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
