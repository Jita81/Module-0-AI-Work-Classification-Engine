output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = aws_eks_cluster.payment-processor_cluster.endpoint
}

output "cluster_name" {
  description = "EKS cluster name"
  value       = aws_eks_cluster.payment-processor_cluster.name
}

output "database_endpoint" {
  description = "RDS database endpoint"
  value       = aws_db_instance.payment-processor_db.endpoint
  sensitive   = true
}

output "redis_endpoint" {
  description = "Redis cluster endpoint"
  value       = aws_elasticache_cluster.payment-processor_cache.cache_nodes[0].address
}
