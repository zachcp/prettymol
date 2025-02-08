;; core loading function. used molnodes code + biotite bond connections.
 (defn load-pdb [code]
   ^struct/AtomArray
   (let [arr (-> code download/download pdbx.CIFFile/read pdbx/get_structure seq first) ]
     (set! (.-bonds arr) (bonds/connect_via_residue_names arr))
     (center-array arr)))



 # (defn- center-array [arr]
 #    (set! (.-coord arr) (np/subtract  (.-coord arr) (databpy/centre (.-coord arr))))
 #    arr)



 # (defn create-basic-material [name stylemap]
 #   (let [mat (doto (bpy.data.materials/new name) (-> .-use_nodes (set! true)))
 #         bsdf (.. mat -node_tree -nodes (get "Principled BSDF"))
 #         styles (merge bsdf-principled-defaults stylemap)]
 #     (doseq [input (.-inputs bsdf)]
 #       (when-not (= (.-type input) "GEOMETRY")
 #         (let [input-name (.-name input)]
 #           (doseq [[key value] styles]
 #             (when (= input-name key)
 #               ;;  (println input " " key " " value "")
 #               (python/setattr input "default_value" value))))))
 #     mat))


 # (defn draw! [arr style-key style-map material]
 #   "take a collection of states corresponding to frames and generate an output"
 #   (let [molname (str (gensym))
 #         [obj _] (molecule/_create_object  arr ** :name molname :style (name style-key))
 #         _ (bl_nodes/create_starting_node_tree obj ** :style (name style-key))
 #         modifier (first (filter #(= (.-type %) "NODES") (vec (.-modifiers obj))))
 #         node-tree (.-node_group modifier)
 #         nodes (.-nodes node-tree)
 #         global-styles (merge default-styles style-map)]
 #     (when-let [style-node (first (filter #(str/includes? (.-name %) "Style") (vec nodes)))]
 #       (doseq [input (.-inputs style-node)]
 #         (when (not= (.-type input) "GEOMETRY")
 #           (let [input-name (.-name input)
 #                 styles (get global-styles style-key)]
 #             (doseq [[key value] styles]
 #               (when (= input-name key)
 #                 (println input " " key " " value "")
 #                 (python/setattr input "default_value" value))))))

 #            ;; Set the material in the node's Material input
 #       (when-let [material-input (first (filter #(= (.-name %) "Material") (.. style-node -inputs)))]
 #         (.. obj -data -materials (append material))
 #         (set! (.-default_value material-input) material)))))


 # (defn filter-amino-acids [arr] (filter/filter_amino_acids arr))

 #  (defn filter-atomname [arr atomname] (= atomname (.get_annotation arr "atom_name")))

 #  (defn filter-canonical-amino-acids [arr] (filter/filter_canonical_amino_acids arr))

 #  (defn filter-canonical-nucleotides [arr] (filter/filter_canonical_nucleotides arr))

 #  (defn filter-carbohydrates [arr] (filter/filter_carbohydrates arr))

 #  (defn filter-chain [arr chain] (= chain (.get_annotation arr "chain_id")))

 #  (defn filter-element [arr element] (= element (.get_annotation arr "element")))

 #  (defn filter-first-altloc [arr] (filter/filter_first_altloc arr))

 #  (defn filter-hetero [arr] (= true (.get_annotation arr "hetero")))

 #  (defn filter-highest-occupancy-altloc [arr] (filter/filter_highest_occupancy_altloc arr))

 #  (defn filter-inscode [arr inscode] (= inscode (.get_annotation arr "ins_code")))

 #  (defn filter-intersection [arr] (filter/filter_intersection arr))

 #  (defn filter-linear-bond-continuity [arr] (filter/filter_linear_bond_continuity arr))

 #  (defn filter-monoatomic-ions [arr] (filter/filter_monoatomic_ions arr))

 #  (defn filter-nucleotides [arr] (filter/filter_nucleotides arr))

 #  (defn filter-peptide-backbone [arr] (filter/filter_peptide_backbone arr))

 #  (defn filter-phosphate-backbone [arr] (filter/filter_phosphate_backbone arr))

 #  (defn filter-polymer [arr] (filter/filter_polymer arr))

 #  (defn filter-resid [arr num] (= num (.get_annotation arr "res_id")))

 #  (defn filter-resname [arr res_name] (= res_name (.get_annotation arr "res_name")))

 #  (defn filter-solvent [arr] (filter/filter_solvent arr))
