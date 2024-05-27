package com.norma_c.graph.backend.services;

import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;
import org.springframework.stereotype.Service;

@Service
public class DatabaseService {
	@PersistenceContext
	private EntityManager entityManager;

	@SuppressWarnings("unchecked")
	public <T> TypedQuery<T> createNativeTypedQuery(
		String query,
		Class<T> castClass
	) {
		return (TypedQuery<T>) entityManager
			.createNativeQuery(query, castClass);
	}

	public static String injectSample(String sample) {
		if (!sample.matches("^\\d+[smhd]$")) {
			throw new IllegalArgumentException(
				"Not SQL-Safe sample: " + sample
			);
		}

		return sample;
	}
}