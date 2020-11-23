export const SyncStatus = Object.freeze({
  Empty: 0,
  Modified: 1,
  AwaitsConfirmation: 2 | 1,
});

function withMeta(init, repr) {
  return {
    status: SyncStatus.Empty,
    value: init,
    repr: repr,
  }
}

export function newFlaw(empty = false) {
  console.error("newFlaw not implemented", empty);
  return withMeta(null, () => "FLAW TODO");
}

export function newEntry(empty = false) {
  const repr = val => val?.title || "";
  if (empty) {
    return withMeta(null, repr);
  } else {
    return withMeta({
      id: null,
      category: newCategory(true),
      category_version: "",
      title: "",
      manufacturer: "",
      year_built: "",
      inspection_signs: "",
      manufacture_info_available: "Keine Angabe",
      easy_access: "Keine Angabe",
      flaws: []
    }, repr);
  }
}

export function newCategory(empty = false) {
  const repr = val => val?.name || "";
  if (empty) {
    return withMeta(null, repr);
  } else {
    return withMeta({
      id: null,
      name: "",
      inspection_standards: []
    });
  }
}

export function newInspectionStandard(empty = false) {
  const repr = val => val?.din || "";
  if (empty) {
    return withMeta(null, repr);
  } else {
    return withMeta({
      id: null,
      din: "",
      description: "",
      has_version: "Nein",
    });
  }
}

export function newFacility(empty = false) {
  const repr = val => val?.name || "";
  if (empty) {
    return withMeta(null, repr);
  } else {
    return withMeta({
      id: null,
      name: "",
      street: "",
      zip_code: "",
      city: ""
    });
  }
}

export function newPerson(empty = false) {
  const repr = val => {
    if (!val) {
      return "";
    } else {
      return `${val.name}, ${val.first_name}`;
    }
  };

  if (empty) {
    return withMeta(null, repr);
  } else {
    return withMeta({
      id: null,
      name: "",
      first_name: "",
      email: "",
      organization: ""
    });
  }
}

export function newOrganization(empty = false) {
  const repr = val => val?.name || "";
  if (empty) {
    return withMeta(null, repr);
  } else {
    return withMeta({
      id: null,
      name: "",
      street: "",
      zip_code: "",
      city: ""
    });
  }
}

export function newProtocol(empty = false) {
  const repr = val => val?.title || "";
  if (empty) {
    return withMeta(null, repr);
  } else {
    return withMeta({
      id: null,
      title: "",
      overview: "",
      facility: newFacility(true),
      inspection_date: "",
      inspector: newPerson(true),
      issuer: newOrganization(true),
      attendees: "",
      entries: [],
    }, repr);
  }
}
