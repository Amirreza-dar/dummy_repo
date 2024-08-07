# Jump Analysis CSV File Format

The generated CSV file captures detailed information about each jump analyzed by the system. Each record in the CSV file represents a single jump and includes the following fields:

- **Left foot delay/score**: This field records the delay or score associated with the left foot during the jump.

- **Right foot delay/score**: Similar to the left foot, this field captures the delay or score associated with the right foot.

- **Jump duration (size of plot)**: This field records the duration of the jump, which may also correspond to the size of the plot visualizing the jump data.

- **Jump validity**: This field indicates the validity of the jump and is categorized into three distinct values:
  - `0`: Ok - The jump is considered successful and meets all the criteria.
  - `1`: Almost Ok - The jump is nearly successful but may have minor issues.
  - `2`: Failed - The jump did not meet the necessary criteria and is considered failed.

Each record in the CSV file adheres to the described format, ensuring a consistent and structured representation of the jump analysis data.
