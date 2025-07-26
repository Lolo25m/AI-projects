import numpy as np
from sklearn.cluster import KMeans

# 1. Original equations: each row is (a, b, c)
equations = np.array([
    [1, 7, 10],   # delta = 49 - 40 = 9   (Real roots - different)
    [1, 2, 1],    # delta = 4 - 4 = 0     (One repeated real root)
    [1, 0, 1],    # delta = 0 - 4 = -4    (Complex roots)
    [1, -3, 2],   # delta = 9 - 8 = 1     (Real roots - different)
    [1, 4, 4],    # delta = 16 - 16 = 0   (One repeated real root)
    [1, 1, 1]     # delta = 1 - 4 = -3    (Complex roots)
])

# 2. Compute delta for each equation: delta = b^2 - 4ac
delta = equations[:,1]**2 - 4*equations[:,0]*equations[:,2]
delta = delta.reshape(-1,1)  # Reshape to column vector for sklearn

# 3. Create KMeans model with 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42)

# 4. Train the model on delta values
kmeans.fit(delta)

# 5. Print each equation and its assigned group
print("Original equations and their classification based on Delta:")
for i, d in enumerate(delta):
    if d[0] < 0:
        group_name = "Delta Negative"
    elif d[0] == 0:
        group_name = "Delta Zero"
    else:
        group_name = "Delta Positive"
    print(f"Equation {i+1}: Delta = {d[0]}, Group: {group_name}")
    """print("Equation", i+1,": Delta =", d[0], "Group:" , group_name)"""

# 6. Link each cluster to its meaning (Negative / Zero / Positive)
cluster_labels = {}
for i in range(3):
    cluster_points = delta[kmeans.labels_ == i]
    avg = np.mean(cluster_points)
    if avg < 0:
        cluster_labels[i] = "Delta Negative"
    elif avg == 0:
        cluster_labels[i] = "Delta Zero"
    else:
        cluster_labels[i] = "Delta Positive"

# 7. Function to predict the group of a new equation
def predict_equation_group(a, b, c):
    delta_new = b**2 - 4*a*c
    cluster = kmeans.predict([[delta_new]])
    label = cluster_labels[cluster[0]]
    return delta_new, label

# 8. Test with a new equation
a_new, b_new, c_new = 1, 6, 5
delta_value, group_label = predict_equation_group(a_new, b_new, c_new)
print(f"\nNew equation: a={a_new}, b={b_new}, c={c_new}")
print(f"Delta = {delta_value}, Classified as: {group_label}")
