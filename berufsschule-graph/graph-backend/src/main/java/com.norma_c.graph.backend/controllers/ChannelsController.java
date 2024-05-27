package com.norma_c.graph.backend.controllers;

import com.norma_c.graph.backend.services.DatabaseService;
import jakarta.annotation.Nullable;
import jakarta.persistence.TypedQuery;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

import static com.norma_c.graph.backend.controllers.ControllersDescriptor.CHANNELS_URL;
import static java.util.stream.Collectors.*;
import static org.springframework.http.ResponseEntity.badRequest;
import static org.springframework.http.ResponseEntity.ok;

@RestController
@RequiredArgsConstructor
public class ChannelsController {
	private final DatabaseService databaseService;

	@GetMapping(CHANNELS_URL)
	public ResponseEntity<List<Channel>> getChannels(
		@RequestParam("unt") @Nullable String unit,
		@RequestParam("max") @Nullable Double maxValue
	) {
		if (unit == null || maxValue == null) {
			return ok(map(databaseService.createNativeTypedQuery("""
					SELECT
						c.id, c.alias, c.unit, c.max_value as maxValue,
						l.alarm_level as alarmLevel, l.value as limitValue
					FROM channels c
					JOIN limits l ON l.channel_id = c.id""",
				ChannelWithSingleLimit.class)
			));
		}

		return ok(map(databaseService.createNativeTypedQuery("""
					SELECT
						c.id, c.alias, c.unit, c.max_value as maxValue,
						l.alarm_level as alarmLevel, l.value as limitValue
					FROM channels c
					JOIN limits l ON l.channel_id = c.id
					WHERE c.unit = :unit
					AND c.max_value <= :maxValue""",
				ChannelWithSingleLimit.class)
			.setParameter("unit", unit)
			.setParameter("maxValue", maxValue)
		));
	}

	@GetMapping(CHANNELS_URL + "/{id}")
	public ResponseEntity<Channel> getChannel(
		@PathVariable("id") String id
	) {
		return ok(map(databaseService.createNativeTypedQuery("""
				SELECT
					c.id, c.alias, c.unit, c.max_value as maxValue,
					l.alarm_level as alarmLevel, l.value as limitValue
				FROM channels c
				JOIN limits l ON l.channel_id = c.id
				WHERE c.id = :id""", ChannelWithSingleLimit.class)
			.setParameter("id", id))
			.getFirst()
		);
	}

	@ExceptionHandler(Exception.class)
	public ResponseEntity<String> handleException(Exception exception) {
		return badRequest().body(exception.getMessage());
	}

	private List<Channel> map(TypedQuery<ChannelWithSingleLimit> query) {
		return query.getResultStream()
			.collect(groupingBy(
				ChannelWithSingleLimit::id,
				collectingAndThen(toList(), list -> new Channel(
					list.getFirst().id(),
					list.getFirst().alias(),
					list.getFirst().unit(),
					list.getFirst().maxValue(),
					list.stream()
						.map(c -> new Limit(c.alarmLevel, c.limitValue))
						.toList()))))
			.values().stream()
			.toList();
	}

	private record ChannelWithSingleLimit(
		String id,
		String alias,
		String unit,
		@Nullable Double maxValue,
		short alarmLevel,
		@Nullable Double limitValue
	) {}

	private record Limit(short alarmLevel, @Nullable Double value) {}

	public record Channel(
		String id,
		String alias,
		String unit,
		@Nullable Double maxValue,
		List<Limit> limits
	) {}
}