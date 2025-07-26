from collections import deque
from typing import List, Optional, Tuple
from itertools import product

# Define action values (in pixels)
actions = {
    "Draw": -15,
    "Light Hit": -3,
    "Medium Hit": -6,
    "Hard Hit": -9,
    "Punch": 2,
    "Bend": 7,
    "Upset": 13,
    "Shrink": 16
}

# Define expandable aliases
action_aliases = {
    "Hit": ["Light Hit", "Medium Hit", "Hard Hit"]
}

# Sort actions by absolute movement power (most impact first)
sorted_action_items = sorted(actions.items(), key=lambda x: abs(x[1]), reverse=True)
sorted_actions = [name for name, _ in sorted_action_items]

def expand_aliases(step_list: List[str]) -> List[List[str]]:
    """Expands alias actions like 'Hit' into all possible real action combinations."""
    expanded_steps = []
    for step in step_list:
        if step in action_aliases:
            expanded_steps.append(action_aliases[step])
        else:
            expanded_steps.append([step])
    return list(product(*expanded_steps))

def bfs_find_optimal_sequence(target_distance: int, required_final_steps: List[str], max_total_depth: int = 14) -> Optional[List[str]]:
    all_variants = expand_aliases(required_final_steps)

    for variant in all_variants:
        required_total = sum(actions[step] for step in variant)
        intermediate_target = -target_distance - required_total  # corrected logic

        max_prefix_depth = max_total_depth - len(variant)
        queue = deque()
        queue.append(([], 0))  # (current_sequence, current_sum)

        while queue:
            seq, total = queue.popleft()

            if len(seq) > max_prefix_depth:
                continue

            if total == intermediate_target:
                full_sequence = seq + list(variant)
                print(f"\n✅ Found sequence (total: {sum(actions[step] for step in full_sequence)} px):")
                for i, step in enumerate(full_sequence):
                    print(f"  Step {i+1}: {step:<10} → {actions[step]:+} px")
                return full_sequence

            for action in sorted_actions:
                queue.append((seq + [action], total + actions[action]))

    print("❌ No valid sequence found.")
    print(f"→ Target distance: {target_distance}")
    print(f"→ Required final steps: {required_final_steps}")
    print(f"→ All variants tried: {len(all_variants)}")
    return None

# Test with example input
target_distance = -83
required_final_steps = ["Bend", "Draw", "Hit"]
bfs_find_optimal_sequence(target_distance, required_final_steps)

###### Bronze
### Rod
# Step 1-8: Shrink     → +16 px
# Step 9: Punch        → +2 px
# Step 10-11: Draw     → -15 px
# Step 12: Bend        → +7 px
### Plate
# Step 1-5: Shrink      → +16 px
# Step 6-8: Bend        → +7 px
# Step 9-11: Light Hit  → -3 px




###### Copper
### Plate
# Step 1-3: Shrink     → +16 px
# Step 4: Upset        → +13 px
# Step 5: Bend         → +7 px
# Step 6-8: Light Hit  → -3 px





###### Bloom
### Refined Wrought Iron
# Step 1-6: Shrink     → +16 px
# Step 7: Bend         → +7 px
# Step 8-10: Light Hit → -3 px

### Wrought Iron Ingot
# Step 1-4: Shrink     → +16 px
# Step 5: Upset        → +13 px
# Step 6: Bend         → +7 px
# Step 7-9: Light Hit  → -3 px





###### Pig Iron
### Carbon Steel
# Step 1-7: Shrink     → +16 px
# Step 8: Bend       → +7 px
# Step 9: Punch      → +2 px
# Step 10-12: Light Hit  → -3 px
### Steel
# Step 1-4: Shrink     → +16 px
# Step 5-6: Upset      → +13 px
# Step 7-9: Light Hit  → -3 px





###### Wrought Iron
### Rod
# Step 1-8: Shrink    → +16 px
# Step 9-10: Draw     → -15 px
# Step 11: Bend       → +7 px

### Plate
# Step 1-4: Shrink    → +16 px
# Step 5: Upset       → +13 px
# Step 6-8: Light Hit → -3 px





###### Brass
### Rod
# Step 1-4: Shrink   → +16 px
# Step 5: Bend       → +7 px
# Step 6: Punch      → +2 px
# Step 7-8: Draw     → -15 px
# Step 9: Bend       → +7 px

### Plate
# Step 1-5: Shrink      → +16 px
# Step 6: Upset         → +13 px
# Step 7: Punch         → +2 px
# Step 8-10: Light Hit  → -3 px